"""
This file is part of nucypher.

nucypher is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nucypher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""


from collections import OrderedDict

from constant_sorrow.constants import (BARE, CONTRACT_NOT_DEPLOYED, FULL, IDLE, NO_BENEFICIARY, NO_DEPLOYER_CONFIGURED)
from eth_typing.evm import ChecksumAddress
from typing import Dict, List, Tuple
from web3 import Web3
from web3.contract import Contract

from nucypher.blockchain.economics import BaseEconomics, StandardTokenEconomics
from nucypher.blockchain.eth.agents import (AdjudicatorAgent, ContractAgency, EthereumContractAgent, MultiSigAgent,
                                            NucypherTokenAgent, PolicyManagerAgent, PreallocationEscrowAgent,
                                            StakingEscrowAgent, WorkLockAgent)
from nucypher.blockchain.eth.constants import DISPATCHER_CONTRACT_NAME, NULL_ADDRESS, STAKING_ESCROW_CONTRACT_NAME
from nucypher.blockchain.eth.decorators import validate_checksum_address
from nucypher.blockchain.eth.interfaces import (
    BlockchainDeployerInterface,
    BlockchainInterfaceFactory,
    VersionedContract,
)
from nucypher.blockchain.eth.registry import AllocationRegistry, BaseContractRegistry


class BaseContractDeployer:

    _interface_class = BlockchainDeployerInterface

    agency = NotImplemented
    contract_name = NotImplemented
    deployment_steps = NotImplemented

    _upgradeable = NotImplemented
    _ownable = NotImplemented
    _proxy_deployer = NotImplemented

    can_be_idle = False

    class ContractDeploymentError(Exception):
        pass

    class ContractNotDeployed(ContractDeploymentError):
        pass

    def __init__(self,
                 registry: BaseContractRegistry,
                 economics: BaseEconomics = None,
                 deployer_address: str = None):

        #
        # Validate
        #
        self.blockchain = BlockchainInterfaceFactory.get_interface()
        if not isinstance(self.blockchain, BlockchainDeployerInterface):
            raise ValueError("No deployer interface connection available.")

        #
        # Defaults
        #
        self.registry = registry
        self.deployment_receipts = OrderedDict()
        self._contract = CONTRACT_NOT_DEPLOYED
        self.__proxy_contract = NotImplemented
        self.__deployer_address = deployer_address
        self.__economics = economics or StandardTokenEconomics()

    @property
    def economics(self) -> BaseEconomics:
        """Read-only access for economics instance."""
        return self.__economics

    @property
    def contract_address(self) -> str:
        if self._contract is CONTRACT_NOT_DEPLOYED:
            raise self.ContractNotDeployed(self.contract_name)
        address = self._contract.address  # type: str
        return address

    @property
    def deployer_address(self):
        return self.__deployer_address

    @property
    def contract(self):
        return self._contract

    @property
    def dispatcher(self):
        return self.__proxy_contract

    def is_deployed(self, contract_version: str = None) -> bool:
        try:
            self.registry.search(contract_name=self.contract_name, contract_version=contract_version)
        except (BaseContractRegistry.UnknownContract, BaseContractRegistry.NoRegistry):
            return False
        else:
            return True

    def check_deployment_readiness(self,
                                   contract_version: str = None,
                                   ignore_deployed=False,
                                   fail=True,
                                   additional_rules: List[Tuple[bool, str]] = None,
                                   ) -> Tuple[bool, list]:
        """
        Iterates through a set of rules required for an ethereum
        contract deployer to be eligible for deployment returning a
        tuple or raising an exception if <fail> is True.

        Returns a tuple containing the boolean readiness result and a list of reasons (if any)
        why the deployer is not ready.

        If fail is set to True, raise a configuration error, instead of returning.
        """

        if not ignore_deployed and contract_version is not None:
            contract_version, _data = self.blockchain.find_raw_contract_data(contract_name=self.contract_name,
                                                                             requested_version=contract_version)

        # Compile rules
        rules = [
            (ignore_deployed or not self.is_deployed(contract_version), f'Contract {self.contract_name}:{contract_version} already deployed'),
            (self.deployer_address is not None, 'No deployer address set.'),
            (self.deployer_address is not NO_DEPLOYER_CONFIGURED, 'No deployer address set.'),
        ]
        if additional_rules:
            rules.extend(additional_rules)

        disqualifications = list()
        for rule_is_satisfied, failure_reason in rules:
            if not rule_is_satisfied:                      # If this rule fails...
                if fail:
                    raise self.ContractDeploymentError(failure_reason)
                disqualifications.append(failure_reason)   # ... here's why

        is_ready = len(disqualifications) == 0
        return is_ready, disqualifications

    def deploy(self, deployment_mode=FULL, gas_limit: int = None, progress: int = None, emitter=None, **overrides) -> dict:
        """
        Provides for the setup, deployment, and initialization of ethereum smart contracts.
        Emits the configured blockchain network transactions for single contract instance publication.
        """
        raise NotImplementedError

    def make_agent(self) -> EthereumContractAgent:
        agent = self.agency(registry=self.registry, contract=self._contract)
        return agent

    def get_latest_enrollment(self) -> VersionedContract:
        """Get the latest enrolled, bare version of the contract from the registry."""
        contract = self.blockchain.get_contract_by_name(contract_name=self.contract_name,
                                                        registry=self.registry,
                                                        use_proxy_address=False,
                                                        enrollment_version='latest')
        return contract

    def _get_deployed_contract(self):
        if self.contract is None or self.contract is CONTRACT_NOT_DEPLOYED:
            proxy_name = None
            if self._proxy_deployer is not NotImplemented:
                proxy_name = self._proxy_deployer.contract_name
            deployed_contract = self.blockchain.get_contract_by_name(contract_name=self.contract_name,
                                                                     registry=self.registry,
                                                                     proxy_name=proxy_name)
        else:
            deployed_contract = self.contract
        return deployed_contract


class OwnableContractMixin:

    _ownable = True

    class ContractNotOwnable(RuntimeError):
        pass

    @property
    def owner(self) -> ChecksumAddress:
        if self._upgradeable:
            # Get the address of the proxy
            contract = self.get_proxy_deployer()
        else:
            # Get the address of the implementation
            contract = self.blockchain.get_contract_by_name(contract_name=self.contract_name, registry=self.registry)
        owner_address = ChecksumAddress(contract.contract.functions.owner().call())  # blockchain read
        return owner_address

    def transfer_ownership(self, new_owner: str, transaction_gas_limit: int = None) -> dict:
        if not self._ownable:
            raise self.ContractNotOwnable(f"{self.contract_name} is not ownable.")

        if self._upgradeable:

            #
            # Upgrade Proxy
            #
            proxy_deployer = self.get_proxy_deployer()
            proxy_contract_function = proxy_deployer.contract.functions.transferOwnership(new_owner)
            receipt = self.blockchain.send_transaction(sender_address=self.deployer_address,
                                                       contract_function=proxy_contract_function,
                                                       transaction_gas_limit=transaction_gas_limit)
        else:
            existing_bare_contract = self.blockchain.get_contract_by_name(contract_name=self.contract_name,
                                                                          registry=self.registry)

            #
            # Upgrade Principal
            #

            contract_function = existing_bare_contract.functions.transferOwnership(new_owner)
            receipt = self.blockchain.send_transaction(sender_address=self.deployer_address,
                                                       contract_function=contract_function,
                                                       transaction_gas_limit=transaction_gas_limit)
        return receipt


class UpgradeableContractMixin:

    _upgradeable = True
    _proxy_deployer = NotImplemented

    class ContractNotUpgradeable(RuntimeError):
        pass
    
    def deploy(self,
               deployment_mode=FULL,
               gas_limit: int = None,
               progress=None,
               contract_version: str = "latest",
               ignore_deployed: bool = False
               ) -> dict:
        """
        Provides for the setup, deployment, and initialization of ethereum smart contracts.
        Emits the configured blockchain network transactions for single contract instance publication.
        """
        if not self._upgradeable:
            raise self.ContractNotUpgradeable(f"{self.contract_name} is not upgradeable.")
        raise NotImplementedError

    def get_principal_contract(self) -> VersionedContract:
        """
        Get the on-chain targeted version of the principal contract directly without assembling it with its proxy.
        """
        if not self._upgradeable:
            raise self.ContractNotUpgradeable(f"{self.contract_name} is not upgradeable.")
        principal_contract = self.blockchain.get_contract_by_name(contract_name=self.contract_name,
                                                                  registry=self.registry,
                                                                  proxy_name=self._proxy_deployer.contract_name,
                                                                  use_proxy_address=False)
        return principal_contract

    def get_proxy_contract(self) -> VersionedContract:  # TODO: Method seems unused and untested
        if not self._upgradeable:
            raise self.ContractNotUpgradeable(f"{self.contract_name} is not upgradeable.")
        principal_contract = self.get_principal_contract()
        proxy_contract = self.blockchain.get_proxy_contract(registry=self.registry,
                                                            target_address=principal_contract.address,
                                                            proxy_name=self._proxy_deployer.contract_name)
        return proxy_contract

    def get_proxy_deployer(self) -> BaseContractDeployer:
        principal_contract = self.get_principal_contract()
        proxy_deployer = self._proxy_deployer(registry=self.registry,
                                              deployer_address=self.deployer_address,
                                              target_contract=principal_contract,
                                              bare=True)  # acquire access to the proxy itself.
        return proxy_deployer

    def retarget(self,
                 target_address: str,
                 confirmations: int,
                 gas_limit: int = None,
                 just_build_transaction: bool = False):
        """
        Directly engage a proxy contract for an existing deployment, executing the proxy's
        upgrade interfaces to verify upgradeability and modify the on-chain contract target.
        """

        if not self._upgradeable:
            raise self.ContractNotUpgradeable(f"{self.contract_name} is not upgradeable.")

        # 1 - Get Proxy Deployer
        proxy_deployer = self.get_proxy_deployer()

        # 2 - Retarget (or build retarget transaction)
        if just_build_transaction:
            transaction = proxy_deployer.build_retarget_transaction(new_target=target_address,
                                                                    gas_limit=gas_limit)
            return transaction
        else:
            receipt = proxy_deployer.retarget(new_target=target_address,
                                              gas_limit=gas_limit,
                                              confirmations=confirmations)
            return receipt

    def upgrade(self,
                confirmations: int,
                gas_limit: int = None,
                contract_version: str = "latest",
                ignore_deployed: bool = False,
                **overrides):
        """
        Deploy a new version of a contract, then engage the proxy contract's upgrade interfaces.
        """

        # 1 - Raise if not all-systems-go #
        if not self._upgradeable:
            raise self.ContractNotUpgradeable(f"{self.contract_name} is not upgradeable.")
        self.check_deployment_readiness(contract_version=contract_version, ignore_deployed=ignore_deployed)

        # 2 - Get Proxy Deployer
        proxy_deployer = self.get_proxy_deployer()

        # 3 - Deploy new version
        new_contract, deploy_receipt = self._deploy_essential(contract_version=contract_version,
                                                              gas_limit=gas_limit,
                                                              confirmations=confirmations,
                                                              **overrides)

        # 4 - Wrap the escrow contract
        wrapped_contract = self.blockchain._wrap_contract(wrapper_contract=proxy_deployer.contract,
                                                          target_contract=new_contract)

        # 5 - Set the new Dispatcher target
        upgrade_receipt = proxy_deployer.retarget(new_target=new_contract.address,
                                                  gas_limit=gas_limit,
                                                  confirmations=confirmations)

        # 6 - Respond
        upgrade_transaction = {'deploy': deploy_receipt, 'retarget': upgrade_receipt}
        self._contract = wrapped_contract  # Switch the contract for the wrapped one
        return upgrade_transaction

    def rollback(self, gas_limit: int = None):
        """
        Execute an existing deployment's proxy contract, engaging the upgrade rollback interfaces,
        modifying the proxy's on-chain contract target to the most recent previous target.
        """

        if not self._upgradeable:
            raise self.ContractNotUpgradeable(f"{self.contract_name} is not upgradeable.")

        proxy_deployer = self.get_proxy_deployer()
        rollback_receipt = proxy_deployer.rollback(gas_limit=gas_limit)

        return rollback_receipt

    def _finish_bare_deployment(self, deployment_receipt: dict, progress=None) -> dict:
        """Used to divert flow control for bare contract deployments."""
        deployment_step_name = self.deployment_steps[0]
        result = {deployment_step_name: deployment_receipt}
        self.deployment_receipts.update(result)
        if progress:
            progress.update(len(self.deployment_steps))  # Update the progress bar to completion.
        return result


class NucypherTokenDeployer(BaseContractDeployer):

    agency = NucypherTokenAgent
    contract_name = agency.contract_name
    deployment_steps = ('contract_deployment', )
    _upgradeable = False
    _ownable = False

    def deploy(self,
               gas_limit: int = None,
               progress=None,
               confirmations: int = 0,
               deployment_mode=FULL,
               ignore_deployed: bool = False,
               emitter=None,
               **overrides) -> dict:
        """
        Deploy and publish the NuCypher Token contract
        to the blockchain network specified in self.blockchain.network.

        Deployment can only ever be executed exactly once!
        """
        if deployment_mode != FULL:
            raise self.ContractDeploymentError(f"{self.contract_name} cannot be deployed in {deployment_mode} mode")

        self.check_deployment_readiness(ignore_deployed=ignore_deployed)
        
        if emitter:
            emitter.message("\nNext Transaction: Token Contract Creation", color='blue', bold=True)

        # WARNING: Order-sensitive!
        constructor_kwargs = {"_totalSupplyOfTokens": self.economics.erc20_total_supply}
        constructor_kwargs.update(overrides)
        constructor_kwargs = {k: v for k, v in constructor_kwargs.items() if v is not None}
        contract, deployment_receipt = self.blockchain.deploy_contract(self.deployer_address,
                                                                       self.registry,
                                                                       self.contract_name,
                                                                       gas_limit=gas_limit,
                                                                       confirmations=confirmations,
                                                                       **constructor_kwargs)
        if progress:
            progress.update(1)
        self._contract = contract
        return {self.deployment_steps[0]: deployment_receipt}


class ProxyContractDeployer(BaseContractDeployer):

    contract_name = NotImplemented
    deployment_steps = ('contract_deployment',)
    _upgradeable = False

    def __init__(self, target_contract: Contract, bare: bool = False, *args, **kwargs):
        self.target_contract = target_contract
        super().__init__(*args, **kwargs)
        if bare:
            self._contract = self.blockchain.get_proxy_contract(registry=self.registry,
                                                                target_address=self.target_contract.address,
                                                                proxy_name=self.contract_name)

    def deploy(self, gas_limit: int = None, progress=None, confirmations: int = 0) -> dict:
        constructor_args = (self.target_contract.address,)
        proxy_contract, receipt = self.blockchain.deploy_contract(self.deployer_address,
                                                                  self.registry,
                                                                  self.contract_name,
                                                                  *constructor_args,
                                                                  gas_limit=gas_limit,
                                                                  confirmations=confirmations)
        if progress:
            progress.update(1)

        self._contract = proxy_contract
        receipts = {self.deployment_steps[0]: receipt}
        self.deployment_receipts.update(receipts)
        return receipts

    def _validate_retarget(self, new_target: str):
        if new_target == self.target_contract.address:
            raise self.ContractDeploymentError(f"{new_target} is already targeted by {self.contract_name}: {self._contract.address}")
        if new_target == self._contract.address:
            raise self.ContractDeploymentError(f"{self.contract_name} {self._contract.address} cannot target itself.")

    def retarget(self,
                 new_target: str,
                 confirmations: int,
                 gas_limit: int = None,
                 ) -> dict:
        self._validate_retarget(new_target)
        upgrade_function = self._contract.functions.upgrade(new_target)
        upgrade_receipt = self.blockchain.send_transaction(contract_function=upgrade_function,
                                                           sender_address=self.deployer_address,
                                                           transaction_gas_limit=gas_limit,
                                                           confirmations=confirmations)
        return upgrade_receipt

    def build_retarget_transaction(self,
                                   new_target: str,
                                   gas_limit: int = None) -> dict:
        self._validate_retarget(new_target)
        upgrade_function = self._contract.functions.upgrade(new_target)
        unsigned_transaction = self.blockchain.build_contract_transaction(contract_function=upgrade_function,
                                                                          sender_address=self.deployer_address,
                                                                          transaction_gas_limit=gas_limit)
        return unsigned_transaction

    def rollback(self, gas_limit: int = None) -> dict:
        origin_args = {}  # TODO: Gas management - #842
        if gas_limit:
            origin_args.update({'gas': gas_limit})

        rollback_function = self._contract.functions.rollback()
        rollback_receipt = self.blockchain.send_transaction(contract_function=rollback_function,
                                                            sender_address=self.deployer_address,
                                                            payload=origin_args)
        return rollback_receipt


class DispatcherDeployer(OwnableContractMixin, ProxyContractDeployer):
    """
    Ethereum smart contract that acts as a proxy to another ethereum contract,
    used as a means of "dispatching" the correct version of the contract to the client
    """

    contract_name = DISPATCHER_CONTRACT_NAME


class StakingEscrowDeployer(BaseContractDeployer, UpgradeableContractMixin, OwnableContractMixin):
    """
    Deploys the StakingEscrow ethereum contract to the blockchain.  Depends on NucypherTokenAgent
    """

    agency = StakingEscrowAgent
    contract_name = agency.contract_name

    can_be_idle = True
    preparation_steps = ('contract_deployment', 'dispatcher_deployment')
    activation_steps = ('approve_reward_transfer', 'initialize')
    deployment_steps = preparation_steps + activation_steps
    _proxy_deployer = DispatcherDeployer

    def __init__(self, test_mode: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dispatcher_contract = None

        token_contract_name = NucypherTokenDeployer.contract_name
        self.token_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                   contract_name=token_contract_name)
        self.test_mode = test_mode

    def _deploy_essential(self, contract_version: str, gas_limit: int = None, confirmations: int = 0, **overrides):
        args = self.economics.staking_deployment_parameters
        constructor_kwargs = {
            "_hoursPerPeriod": args[0],
            "_issuanceDecayCoefficient": args[1],
            "_lockDurationCoefficient1": args[2],
            "_lockDurationCoefficient2": args[3],
            "_maximumRewardedPeriods": args[4],
            "_firstPhaseTotalSupply": args[5],
            "_firstPhaseMaxIssuance": args[6],
            "_minLockedPeriods": args[7],
            "_minAllowableLockedTokens": args[8],
            "_maxAllowableLockedTokens": args[9],
            "_minWorkerPeriods": args[10],
            "_isTestContract": self.test_mode
        }
        constructor_kwargs.update(overrides)
        constructor_kwargs = {k: v for k, v in constructor_kwargs.items() if v is not None}
        # Force use of the token address from the registry
        constructor_kwargs.update({"_token": self.token_contract.address})
        the_escrow_contract, deploy_receipt = self.blockchain.deploy_contract(
            self.deployer_address,
            self.registry,
            self.contract_name,
            gas_limit=gas_limit,
            contract_version=contract_version,
            confirmations=confirmations,
            **constructor_kwargs
        )

        return the_escrow_contract, deploy_receipt

    def deploy(self,
               deployment_mode=FULL,
               gas_limit: int = None,
               progress=None,
               contract_version: str = "latest",
               ignore_deployed: bool = False,
               confirmations: int = 0,
               emitter=None,
               **overrides
               ) -> dict:
        """
        Deploy and publish the StakingEscrow contract
        to the blockchain network specified in self.blockchain.network.

        Emits the following blockchain network transactions:
            - StakingEscrow contract deployment
            - StakingEscrow dispatcher deployment
            - Transfer reward tokens origin to StakingEscrow contract
            - StakingEscrow contract initialization

        Returns transaction receipts in a dict.
        """

        if deployment_mode not in (BARE, IDLE, FULL):
            raise ValueError(f"Invalid deployment mode ({deployment_mode})")

        # Raise if not all-systems-go
        self.check_deployment_readiness(contract_version=contract_version, ignore_deployed=ignore_deployed)

        # Build deployment arguments
        origin_args = {}
        if gas_limit:
            origin_args.update({'gas': gas_limit})  # TODO: Gas Management - #842

        # 1 - Deploy #
        if emitter:
            emitter.message(f"\nNext Transaction: {self.contract_name} Contract Creation", color='blue', bold=True)
        the_escrow_contract, deploy_receipt = self._deploy_essential(contract_version=contract_version,
                                                                     gas_limit=gas_limit,
                                                                     confirmations=confirmations,
                                                                     **overrides)

        # This is the end of bare deployment.
        if deployment_mode is BARE:
            self._contract = the_escrow_contract
            receipts = self._finish_bare_deployment(deployment_receipt=deploy_receipt, progress=progress)
            return receipts

        if progress:
            progress.update(1)

        # 2 - Deploy the dispatcher used for updating this contract #
        if emitter:
            emitter.message(f"\nNext Transaction: {DispatcherDeployer.contract_name} Contract Creation for {self.contract_name}", color='blue', bold=True)
        dispatcher_deployer = DispatcherDeployer(registry=self.registry,
                                                 target_contract=the_escrow_contract,
                                                 deployer_address=self.deployer_address)

        dispatcher_receipts = dispatcher_deployer.deploy(gas_limit=gas_limit, confirmations=confirmations)
        dispatcher_deploy_receipt = dispatcher_receipts[dispatcher_deployer.deployment_steps[0]]
        if progress:
            progress.update(1)

        # Cache the dispatcher contract
        dispatcher_contract = dispatcher_deployer.contract
        self.__dispatcher_contract = dispatcher_contract

        # Wrap the escrow contract
        wrapped_escrow_contract = self.blockchain._wrap_contract(dispatcher_contract,
                                                                 target_contract=the_escrow_contract)

        # Switch the contract for the wrapped one
        self._contract = wrapped_escrow_contract

        preparation_receipts = dict(zip(self.preparation_steps, (deploy_receipt, dispatcher_deploy_receipt)))
        self.deployment_receipts = preparation_receipts

        # 3 & 4 - Activation
        if deployment_mode is IDLE:
            # This is the end of deployment without activation: the contract is now idle, waiting for activation
            return preparation_receipts
        else:  # deployment_mode is FULL
            activation_receipts = self.activate(gas_limit=gas_limit,
                                                progress=progress,
                                                confirmations=confirmations,
                                                emitter=emitter)
            self.deployment_receipts.update(activation_receipts)
            return self.deployment_receipts

    def activate(self, gas_limit: int = None, progress=None, emitter=None, confirmations: int = 0):

        self._contract = self._get_deployed_contract()
        if not self.ready_to_activate:
            raise self.ContractDeploymentError(f"This StakingEscrow ({self._contract.address}) cannot be activated")

        origin_args = {}
        if gas_limit:
            origin_args.update({'gas': gas_limit})  # TODO: #842 - Gas Management

        # 3 - Approve transferring the reward supply tokens to StakingEscrow #
        if emitter:
            emitter.message(f"\nNext Transaction: Approve Transfer to {self.contract_name}", color='blue', bold=True)
        approve_reward_function = self.token_contract.functions.approve(self._contract.address,
                                                                        self.economics.erc20_reward_supply)

        # TODO: Confirmations / Successful Transaction Indicator / Events ??  - #1193, #1194
        approve_reward_receipt = self.blockchain.send_transaction(contract_function=approve_reward_function,
                                                                  sender_address=self.deployer_address,
                                                                  confirmations=confirmations,
                                                                  payload=origin_args)
        if progress:
            progress.update(1)

        # 4 - Initialize the StakingEscrow contract
        if emitter:
            emitter.message(f"\nNext Transaction: {self.contract_name} Initialization", color='blue', bold=True)
        init_function = self._contract.functions.initialize(self.economics.erc20_reward_supply, self.deployer_address)
        init_receipt = self.blockchain.send_transaction(contract_function=init_function,
                                                        sender_address=self.deployer_address,
                                                        confirmations=confirmations,
                                                        payload=origin_args)
        if progress:
            progress.update(1)

        activation_receipts = dict(zip(self.activation_steps, (approve_reward_receipt, init_receipt)))
        return activation_receipts

    @property
    def ready_to_activate(self) -> bool:
        try:
            deployed_contract = self._get_deployed_contract()
        except self.blockchain.UnknownContract:
            return False

        # TODO: Consider looking for absence of Initialized event - see #1193
        # This mimics initialization pre-condition in Issuer (StakingEscrow's base contract)
        current_minting_period = deployed_contract.functions.currentMintingPeriod().call()
        return current_minting_period == 0

    @property
    def is_active(self) -> bool:
        try:
            deployed_contract = self._get_deployed_contract()
        except self.blockchain.UnknownContract:
            return False

        # TODO: Consider looking for Initialized event - see #1193
        # This mimics isInitialized() modifier in Issuer (StakingEscrow's base contract)
        current_minting_period = deployed_contract.functions.currentMintingPeriod().call()
        return current_minting_period != 0


class PolicyManagerDeployer(BaseContractDeployer, UpgradeableContractMixin, OwnableContractMixin):
    """
    Depends on StakingEscrow and NucypherTokenAgent
    """

    agency = PolicyManagerAgent
    contract_name = agency.contract_name
    deployment_steps = ('deployment', 'dispatcher_deployment', 'set_policy_manager')
    _proxy_deployer = DispatcherDeployer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        proxy_name = StakingEscrowDeployer._proxy_deployer.contract_name
        staking_contract_name = StakingEscrowDeployer.contract_name
        self.staking_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                     contract_name=staking_contract_name,
                                                                     proxy_name=proxy_name)

    def check_deployment_readiness(self, *args, **kwargs) -> Tuple[bool, list]:
        staking_escrow_owner = self.staking_contract.functions.owner().call()
        policy_manager_deployment_rules = [
            (self.deployer_address == staking_escrow_owner,
             f'{self.contract_name} must be deployed by the owner of {STAKING_ESCROW_CONTRACT_NAME} ({staking_escrow_owner})')
        ]
        return super().check_deployment_readiness(additional_rules=policy_manager_deployment_rules, *args, **kwargs)

    def _deploy_essential(self, contract_version: str, gas_limit: int = None, confirmations: int = 0) -> tuple:
        constructor_kwargs = {"_escrow": self.staking_contract.address}
        policy_manager_contract, deploy_receipt = self.blockchain.deploy_contract(self.deployer_address,
                                                                                  self.registry,
                                                                                  self.contract_name,
                                                                                  gas_limit=gas_limit,
                                                                                  contract_version=contract_version,
                                                                                  confirmations=confirmations,
                                                                                  **constructor_kwargs)
        return policy_manager_contract, deploy_receipt

    def deploy(self,
               deployment_mode=FULL,
               gas_limit: int = None,
               progress=None,
               contract_version: str = "latest",
               ignore_deployed: bool = False,
               confirmations: int = 0,
               emitter=None,
               ) -> Dict[str, dict]:

        if deployment_mode not in (BARE, IDLE, FULL):
            raise ValueError(f"Invalid deployment mode ({deployment_mode})")

        self.check_deployment_readiness(contract_version=contract_version, ignore_deployed=ignore_deployed)

        # Creator deploys the policy manager
        if emitter:
            emitter.message(f"\nNext Transaction: {self.contract_name} Contract Creation", color='blue', bold=True)
        policy_manager_contract, deploy_receipt = self._deploy_essential(contract_version=contract_version,
                                                                         gas_limit=gas_limit,
                                                                         confirmations=confirmations)

        # This is the end of bare deployment.
        if deployment_mode is BARE:
            self._contract = policy_manager_contract
            return self._finish_bare_deployment(deployment_receipt=deploy_receipt,
                                                progress=progress)

        if progress:
            progress.update(1)  # how YOU doin?
        if emitter:
            emitter.message(f"\nNext Transaction: {self._proxy_deployer.contract_name} Contract Creation for {self.contract_name}", color='blue', bold=True)

        proxy_deployer = self._proxy_deployer(registry=self.registry,
                                              target_contract=policy_manager_contract,
                                              deployer_address=self.deployer_address)

        proxy_deploy_receipt = proxy_deployer.deploy(gas_limit=gas_limit, confirmations=confirmations)
        proxy_deploy_receipt = proxy_deploy_receipt[proxy_deployer.deployment_steps[0]]
        if progress:
            progress.update(1)

        # Cache the dispatcher contract
        proxy_contract = proxy_deployer.contract
        self.__proxy_contract = proxy_contract

        # Wrap the PolicyManager contract, and use this wrapper
        wrapped_contract = self.blockchain._wrap_contract(wrapper_contract=proxy_contract,
                                                          target_contract=policy_manager_contract)

        # Configure the StakingEscrow contract by setting the PolicyManager
        tx_args = {}
        if gas_limit:
            tx_args.update({'gas': gas_limit})  # TODO: #842

        if emitter:
            emitter.message(f"\nNext Transaction: Set Policy Manager on {self.staking_contract.address}", color='blue', bold=True)
        set_policy_manager_function = self.staking_contract.functions.setPolicyManager(wrapped_contract.address)
        set_policy_manager_receipt = self.blockchain.send_transaction(contract_function=set_policy_manager_function,
                                                                      sender_address=self.deployer_address,
                                                                      confirmations=confirmations,
                                                                      payload=tx_args)
        if progress:
            progress.update(1)

        # Gather the transaction receipts
        ordered_receipts = (deploy_receipt, proxy_deploy_receipt, set_policy_manager_receipt)
        deployment_receipts = dict(zip(self.deployment_steps, ordered_receipts))

        self.deployment_receipts = deployment_receipts
        self._contract = wrapped_contract
        return deployment_receipts

    def set_fee_rate_range(self,
                           minimum: int,
                           default: int,
                           maximum: int,
                           gas_limit: int = None,
                           confirmations: int = 0) -> dict:

        if minimum > default or default > maximum:
            raise ValueError(f"Default fee rate ({default}) must fall within the global fee range by satisfying the condition: "
                             f"minimum ({minimum}) <= default ({default}) <= maximum ({maximum})")

        policy_manager = self.blockchain.get_contract_by_name(registry=self.registry,
                                                              contract_name=self.contract_name,
                                                              proxy_name=self._proxy_deployer.contract_name)

        tx_args = {}
        if gas_limit:
            tx_args.update({'gas': gas_limit})  # TODO: Gas management - 842
        set_range_function = policy_manager.functions.setFeeRateRange(minimum, default, maximum)
        set_range_receipt = self.blockchain.send_transaction(contract_function=set_range_function,
                                                             sender_address=self.deployer_address,
                                                             payload=tx_args,
                                                             confirmations=confirmations)

        return set_range_receipt


class StakingInterfaceRouterDeployer(OwnableContractMixin, ProxyContractDeployer):

    contract_name = 'StakingInterfaceRouter'

    # Overwrites rollback method from ProxyContractDeployer since StakingInterfaceRouter doesn't support rollback
    def rollback(self, gas_limit: int = None) -> dict:
        raise NotImplementedError


class StakingInterfaceDeployer(BaseContractDeployer, UpgradeableContractMixin, OwnableContractMixin):

    contract_name = 'StakingInterface'
    deployment_steps = ('contract_deployment', 'router_deployment')
    number_of_deployment_transactions = 2
    _proxy_deployer = StakingInterfaceRouterDeployer

    # _ownable = False  # TODO: This contract is not truly ownable but we need the logic of the mixin to execute

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        token_contract_name = NucypherTokenDeployer.contract_name
        self.token_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                   contract_name=token_contract_name)

        staking_contract_name = StakingEscrowDeployer.contract_name
        staking_proxy_name = StakingEscrowDeployer._proxy_deployer.contract_name
        self.staking_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                     contract_name=staking_contract_name,
                                                                     proxy_name=staking_proxy_name)

        policy_contract_name = PolicyManagerDeployer.contract_name
        policy_proxy_name = PolicyManagerDeployer._proxy_deployer.contract_name
        self.policy_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                    contract_name=policy_contract_name,
                                                                    proxy_name=policy_proxy_name)

        worklock_name = WorklockDeployer.contract_name
        try:
            self.worklock_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                          contract_name=worklock_name)
        except BaseContractRegistry.UnknownContract:
            self.worklock_contract = None

    def _deploy_essential(self, contract_version: str, gas_limit: int = None, confirmations: int = 0):
        """Note: These parameters are order-sensitive"""
        worklock_address = self.worklock_contract.address if self.worklock_contract else NULL_ADDRESS
        constructor_args = (self.token_contract.address,
                            self.staking_contract.address,
                            self.policy_contract.address,
                            worklock_address)

        contract, deployment_receipt = self.blockchain.deploy_contract(self.deployer_address,
                                                                       self.registry,
                                                                       self.contract_name,
                                                                       *constructor_args,
                                                                       gas_limit=gas_limit,
                                                                       contract_version=contract_version,
                                                                       confirmations=confirmations)
        return contract, deployment_receipt

    def deploy(self,
               deployment_mode=FULL,
               gas_limit: int = None,
               progress=None,
               contract_version: str = "latest",
               ignore_deployed: bool = False,
               confirmations: int = 0,
               emitter = None
               ) -> dict:
        """
        Deploys a new StakingInterface contract, and a new StakingInterfaceRouter, targeting the former.
        This is meant to be called only once per general deployment.
        """

        if deployment_mode not in (BARE, IDLE, FULL):
            raise ValueError(f"Invalid deployment mode ({deployment_mode})")

        self.check_deployment_readiness(contract_version=contract_version, ignore_deployed=ignore_deployed)

        # 1 - StakingInterface
        if emitter:
            emitter.message(f"\nNext Transaction: {self.contract_name} Contract Creation", color='blue', bold=True)
        staking_interface_contract, deployment_receipt = self._deploy_essential(contract_version=contract_version,
                                                                                gas_limit=gas_limit,
                                                                                confirmations=confirmations)

        # This is the end of bare deployment.
        if deployment_mode is BARE:
            self._contract = staking_interface_contract
            return self._finish_bare_deployment(deployment_receipt=deployment_receipt,
                                                progress=progress)

        if progress:
            progress.update(1)

        # 2 - StakingInterfaceRouter
        if emitter:
            emitter.message(f"\nNext Transaction: {self._proxy_deployer.contract_name} deployment for {self.contract_name}", color='blue', bold=True)
        router_deployer = self._proxy_deployer(registry=self.registry,
                                               deployer_address=self.deployer_address,
                                               target_contract=staking_interface_contract)

        router_deployment_receipts = router_deployer.deploy(gas_limit=gas_limit)
        router_deployment_receipt = router_deployment_receipts[router_deployer.deployment_steps[0]]
        if progress:
            progress.update(1)

        # Gather the transaction receipts
        ordered_receipts = (deployment_receipt, router_deployment_receipt)
        deployment_receipts = dict(zip(self.deployment_steps, ordered_receipts))

        self._contract = staking_interface_contract
        return deployment_receipts


class PreallocationEscrowDeployer(BaseContractDeployer, UpgradeableContractMixin, OwnableContractMixin):
    # TODO: Why does PreallocationEscrowDeployer has an UpgradeableContractMixin?

    agency = PreallocationEscrowAgent
    contract_name = agency.contract_name
    deployment_steps = ('contract_deployment', 'transfer_ownership', 'initial_deposit')
    _router_deployer = StakingInterfaceRouterDeployer
    __allocation_registry = AllocationRegistry

    @validate_checksum_address
    def __init__(self,
                 allocation_registry: AllocationRegistry = None,
                 sidekick_address: str = None,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                   contract_name=NucypherTokenDeployer.contract_name)
        dispatcher_name = StakingEscrowDeployer._proxy_deployer.contract_name
        self.staking_escrow_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                            contract_name=StakingEscrowDeployer.contract_name,
                                                                            proxy_name=dispatcher_name)
        self.__beneficiary_address = NO_BENEFICIARY
        self.__allocation_registry = allocation_registry or self.__allocation_registry()
        self.sidekick_address = sidekick_address

    def make_agent(self) -> 'PreallocationEscrowAgent':
        if self.__beneficiary_address is NO_BENEFICIARY:
            raise self.ContractDeploymentError("No beneficiary assigned to {}".format(self.contract.address))
        agent = self.agency(registry=self.registry,
                            beneficiary=self.__beneficiary_address,
                            allocation_registry=self.__allocation_registry)
        return agent

    @property
    def allocation_registry(self):
        return self.__allocation_registry

    @validate_checksum_address
    def assign_beneficiary(self, checksum_address: str, use_sidekick: bool = False, progress=None) -> dict:
        """Relinquish ownership of a PreallocationEscrow deployment to the beneficiary"""
        deployer_address = self.sidekick_address if use_sidekick else self.deployer_address
        # TODO: #842 - Gas Management
        payload = {'gas': 500_000}
        transfer_owner_function = self.contract.functions.transferOwnership(checksum_address)
        receipt = self.blockchain.send_transaction(contract_function=transfer_owner_function,
                                                   sender_address=deployer_address,
                                                   payload=payload)
        self.__beneficiary_address = checksum_address
        self.deployment_receipts.update({self.deployment_steps[1]: receipt})
        if progress:
            progress.update(1)
        return receipt

    def initial_deposit(self, value: int, duration_seconds: int, progress=None):
        """Allocate an amount of tokens with lock time in seconds"""
        # Initial deposit transfer, using NuCypherToken.approveAndCall()
        call_data = Web3.toBytes(duration_seconds)  # Additional parameters to PreallocationEscrow.initialDeposit()
        approve_and_call = self.token_contract.functions.approveAndCall(self.contract.address, value, call_data)
        approve_and_call_receipt = self.blockchain.send_transaction(contract_function=approve_and_call,
                                                                    sender_address=self.deployer_address)  # TODO: Gas  - #842

        self.deployment_receipts.update({self.deployment_steps[2]: approve_and_call_receipt})

        if progress:
            progress.update(1)

    def enroll_principal_contract(self):
        if self.__beneficiary_address is NO_BENEFICIARY:
            raise self.ContractDeploymentError("No beneficiary assigned to {}".format(self.contract.address))
        self.__allocation_registry.enroll(beneficiary_address=self.__beneficiary_address,
                                          contract_address=self.contract.address,
                                          contract_abi=self.contract.abi)

    def deploy(self,
               gas_limit: int = None,
               use_sidekick: bool = False,
               progress=None,
               ignore_deployed: bool = False,
               emitter=None
               ) -> dict:

        """Deploy a new instance of PreallocationEscrow to the blockchain."""
        self.check_deployment_readiness(ignore_deployed=ignore_deployed)
        router_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                               contract_name=self._router_deployer.contract_name)
        constructor_args = (router_contract.address,)

        deployer_address = self.sidekick_address if use_sidekick else self.deployer_address
        self._contract, deploy_receipt = self.blockchain.deploy_contract(deployer_address,
                                                                         self.registry,
                                                                         self.contract_name,
                                                                         *constructor_args,
                                                                         gas_limit=gas_limit,
                                                                         enroll=False)
        if progress:
            progress.update(1)

        self.deployment_receipts.update({self.deployment_steps[0]: deploy_receipt})
        return deploy_receipt

    def get_contract_abi(self):
        contract_factory = self.blockchain.get_contract_factory(contract_name=self.contract_name)
        abi = contract_factory.abi
        return abi


class AdjudicatorDeployer(BaseContractDeployer, UpgradeableContractMixin, OwnableContractMixin):

    agency = AdjudicatorAgent
    contract_name = agency.contract_name
    deployment_steps = ('contract_deployment', 'dispatcher_deployment', 'set_adjudicator')
    _proxy_deployer = DispatcherDeployer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        staking_contract_name = StakingEscrowDeployer.contract_name
        proxy_name = StakingEscrowDeployer._proxy_deployer.contract_name
        self.staking_contract = self.blockchain.get_contract_by_name(registry=self.registry,
                                                                     contract_name=staking_contract_name,
                                                                     proxy_name=proxy_name)

    def check_deployment_readiness(self, *args, **kwargs) -> Tuple[bool, list]:
        staking_escrow_owner = self.staking_contract.functions.owner().call()
        adjudicator_deployment_rules = [
            (self.deployer_address == staking_escrow_owner,
             f'{self.contract_name} must be deployed by the owner of {STAKING_ESCROW_CONTRACT_NAME} ({staking_escrow_owner})')
        ]
        return super().check_deployment_readiness(additional_rules=adjudicator_deployment_rules, *args, **kwargs)

    def _deploy_essential(self, contract_version: str, gas_limit: int = None, confirmations: int = 0, **overrides):
        args = self.economics.slashing_deployment_parameters
        constructor_kwargs = {
            "_hashAlgorithm": args[0],
            "_basePenalty": args[1],
            "_penaltyHistoryCoefficient": args[2],
            "_percentagePenaltyCoefficient": args[3],
            "_rewardCoefficient": args[4]
        }
        constructor_kwargs.update(overrides)
        constructor_kwargs = {k: v for k, v in constructor_kwargs.items() if v is not None}
        # Force use of the escrow address from the registry
        constructor_kwargs.update({"_escrow": self.staking_contract.address})
        adjudicator_contract, deploy_receipt = self.blockchain.deploy_contract(self.deployer_address,
                                                                               self.registry,
                                                                               self.contract_name,
                                                                               gas_limit=gas_limit,
                                                                               confirmations=confirmations,
                                                                               contract_version=contract_version,
                                                                               **constructor_kwargs)
        return adjudicator_contract, deploy_receipt

    def deploy(self,
               deployment_mode=FULL,
               gas_limit: int = None,
               progress=None,
               contract_version: str = "latest",
               ignore_deployed: bool = False,
               emitter=None,
               confirmations: int = 0,
               **overrides) -> Dict[str, str]:

        if deployment_mode not in (BARE, IDLE, FULL):
            raise ValueError(f"Invalid deployment mode ({deployment_mode})")

        self.check_deployment_readiness(contract_version=contract_version, ignore_deployed=ignore_deployed)

        # 1 - Deploy Contract
        if emitter:
            emitter.message(f"\nNext Transaction: {self.contract_name} Contract Creation", color='blue', bold=True)
        adjudicator_contract, deploy_receipt = self._deploy_essential(contract_version=contract_version,
                                                                      gas_limit=gas_limit,
                                                                      confirmations=confirmations,
                                                                      **overrides)

        # This is the end of bare deployment.
        if deployment_mode is BARE:
            self._contract = adjudicator_contract
            return self._finish_bare_deployment(deployment_receipt=deploy_receipt,
                                                progress=progress)

        if progress:
            progress.update(1)

        # 2 - Deploy Proxy
        if emitter:
            emitter.message(f"\nNext Transaction: {self._proxy_deployer.contract_name} Contract Creation for {self.contract_name}", color='blue', bold=True)
        proxy_deployer = self._proxy_deployer(registry=self.registry,
                                              target_contract=adjudicator_contract,
                                              deployer_address=self.deployer_address)

        proxy_deploy_receipts = proxy_deployer.deploy(gas_limit=gas_limit, confirmations=confirmations)
        proxy_deploy_receipt = proxy_deploy_receipts[proxy_deployer.deployment_steps[0]]
        if progress:
            progress.update(1)

        # Cache the dispatcher contract
        proxy_contract = proxy_deployer.contract
        self.__proxy_contract = proxy_contract

        # Wrap the escrow contract
        wrapped = self.blockchain._wrap_contract(proxy_contract, target_contract=adjudicator_contract)

        # Switch the contract for the wrapped one
        adjudicator_contract = wrapped

        # 3 - Configure the StakingEscrow contract by setting the Adjudicator
        if emitter:
            emitter.message(f"\nNext Transaction: SetAdjudicator on {self.staking_contract.address}", color='blue', bold=True)
        set_adjudicator_function = self.staking_contract.functions.setAdjudicator(adjudicator_contract.address)
        set_adjudicator_receipt = self.blockchain.send_transaction(contract_function=set_adjudicator_function,
                                                                   sender_address=self.deployer_address,
                                                                   confirmations=confirmations,
                                                                   transaction_gas_limit=gas_limit)
        if progress:
            progress.update(1)

        # Gather the transaction receipts
        ordered_receipts = (deploy_receipt, proxy_deploy_receipt, set_adjudicator_receipt)
        deployment_receipts = dict(zip(self.deployment_steps, ordered_receipts))

        self.deployment_receipts = deployment_receipts
        self._contract = adjudicator_contract

        return deployment_receipts


class WorklockDeployer(BaseContractDeployer):

    agency = WorkLockAgent
    contract_name = agency.contract_name
    deployment_steps = ('contract_deployment', 'bond_escrow', 'approve_funding', 'fund_worklock')
    _upgradeable = False

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.token_agent = ContractAgency.get_agent(NucypherTokenAgent, registry=self.registry)  # type: NucypherTokenAgent
        self.staking_agent = ContractAgency.get_agent(StakingEscrowAgent, registry=self.registry)  # type: StakingEscrowAgent

    def _deploy_essential(self, gas_limit: int = None, confirmations: int = 0):
        # Deploy
        constructor_args = (self.token_agent.contract_address,
                            self.staking_agent.contract_address,
                            *self.economics.worklock_deployment_parameters)

        worklock_contract, receipt = self.blockchain.deploy_contract(self.deployer_address,
                                                                     self.registry,
                                                                     self.contract_name,
                                                                     *constructor_args,
                                                                     gas_limit=gas_limit,
                                                                     confirmations=confirmations)

        self._contract = worklock_contract
        return worklock_contract, receipt

    def deploy(self,
               gas_limit: int = None, 
               progress=None, 
               confirmations: int = 0,
               deployment_mode=FULL,
               ignore_deployed: bool = False,
               emitter=None,
               ) -> Dict[str, dict]:

        if deployment_mode != FULL:
            raise self.ContractDeploymentError(f"{self.contract_name} cannot be deployed in {deployment_mode} mode")

        staking_escrow_rule = [
            (self.staking_agent.worklock == NULL_ADDRESS or self.staking_agent.is_test_contract,
             f"StakingEscrow already has a WorkLock reference ({self.staking_agent.worklock})")
        ]
        self.check_deployment_readiness(ignore_deployed=ignore_deployed, additional_rules=staking_escrow_rule)

        # Essential
        if emitter:
            emitter.message(f"\nNext Transaction: {self.contract_name} Contract Creation", color='blue', bold=True)
        worklock_contract, deployment_receipt = self._deploy_essential(gas_limit=gas_limit, confirmations=confirmations)
        if progress:
            progress.update(1)

        # Bonding
        if emitter:
            emitter.message(f"\nNext Transaction: Set Work Lock on {self.staking_agent.contract_address}", color='blue', bold=True)
        bonding_function = self.staking_agent.contract.functions.setWorkLock(worklock_contract.address)
        bonding_receipt = self.blockchain.send_transaction(sender_address=self.deployer_address,
                                                           contract_function=bonding_function,
                                                           confirmations=confirmations)
        if progress:
            progress.update(1)

        # Funding
        approve_receipt, funding_receipt = self.fund(sender_address=self.deployer_address,
                                                     progress=progress,
                                                     confirmations=confirmations,
                                                     emitter=emitter)

        # Gather the transaction hashes
        self.deployment_receipts = dict(zip(self.deployment_steps, (deployment_receipt,
                                                                    bonding_receipt,
                                                                    approve_receipt,
                                                                    funding_receipt)))
        return self.deployment_receipts

    def fund(self, sender_address: str, progress=None, confirmations: int = 0, emitter=None) -> Tuple[dict, dict]:
        """
        Convenience method for funding the contract and establishing the
        total worklock lot value to be auctioned.
        """
        supply = int(self.economics.worklock_supply)

        token_agent = ContractAgency.get_agent(NucypherTokenAgent, registry=self.registry)
        if emitter:
            emitter.message(f"\nNext Transaction: Approve Token Transfer to {self.contract_name}", color='blue', bold=True)
        approve_function = token_agent.contract.functions.approve(self.contract_address, supply)
        approve_receipt = self.blockchain.send_transaction(contract_function=approve_function,
                                                           sender_address=sender_address,
                                                           confirmations=confirmations)

        if progress:
            progress.update(1)

        if emitter:
            emitter.message(f"\nNext Transaction: Transfer Tokens to {self.contract_name}", color='blue', bold=True)
        funding_function = self.contract.functions.tokenDeposit(supply)
        funding_receipt = self.blockchain.send_transaction(contract_function=funding_function,
                                                           sender_address=sender_address,
                                                           confirmations=confirmations)

        if progress:
            progress.update(1)

        return approve_receipt, funding_receipt


class MultiSigDeployer(BaseContractDeployer):

    agency = MultiSigAgent
    contract_name = agency.contract_name
    deployment_steps = ('contract_deployment', )
    _upgradeable = False

    MAX_OWNER_COUNT = 50  # Hard-coded limit in MultiSig contract

    def _deploy_essential(self, threshold: int, owners: List[str], gas_limit: int = None, confirmations: int = 0):
        if not (0 < threshold <= len(owners) <= self.MAX_OWNER_COUNT):
            raise ValueError(f"Parameters threshold={threshold} and len(owners)={len(owners)} don't satisfy inequality "
                             f"0 < threshold <= len(owners) <= {self.MAX_OWNER_COUNT}")
        if NULL_ADDRESS in owners:
            raise ValueError("The null address is not allowed as an owner")
        if len(owners) != len(set(owners)):
            raise ValueError("Can't use the same owner address more than once")

        constructor_args = (threshold, owners)

        multisig_contract, deploy_receipt = self.blockchain.deploy_contract(self.deployer_address,
                                                                            self.registry,
                                                                            self.contract_name,
                                                                            *constructor_args,
                                                                            gas_limit=gas_limit,
                                                                            confirmations=confirmations)
        return multisig_contract, deploy_receipt

    def deploy(self,
               deployment_mode=FULL,
               gas_limit: int = None,
               progress=None,
               ignore_deployed: bool = False,
               emitter=None,
               *args, **kwargs
               ) -> dict:

        if deployment_mode != FULL:
            raise self.ContractDeploymentError(f"{self.contract_name} cannot be deployed in {deployment_mode} mode")

        self.check_deployment_readiness(ignore_deployed=ignore_deployed)

        if emitter:
            emitter.message(f"\nNext Transaction: {self.contract_name} Contract Creation", color='blue', bold=True)
        multisig_contract, deploy_receipt = self._deploy_essential(gas_limit=gas_limit, *args, **kwargs)

        # Update the progress bar
        if progress:
            progress.update(1)

        # Gather the transaction receipts
        self.deployment_receipts.update({self.deployment_steps[0]: deploy_receipt})
        self._contract = multisig_contract
        return self.deployment_receipts
