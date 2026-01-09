import inspect
from typing import Dict, Optional, Type, List, Any
from spectragraph_core.core.transform_base import Transform

# Domain-related transforms (optional imports - keep startup robust)
try:
    from spectragraph_transforms.domain.to_subdomains import SubdomainTransform
except Exception:
    SubdomainTransform = None
try:
    from spectragraph_transforms.domain.to_whois import WhoisTransform
except Exception:
    WhoisTransform = None
try:
    from spectragraph_transforms.domain.to_ip import ResolveTransform
except Exception:
    ResolveTransform = None
try:
    from spectragraph_transforms.domain.to_website import DomainToWebsiteTransform
except Exception:
    DomainToWebsiteTransform = None
try:
    from spectragraph_transforms.domain.to_root_domain import DomainToRootDomain
except Exception:
    DomainToRootDomain = None
try:
    from spectragraph_transforms.domain.to_asn import DomainToAsnTransform
except Exception:
    DomainToAsnTransform = None
try:
    from spectragraph_transforms.domain.to_history import DomainToHistoryTransform
except Exception:
    DomainToHistoryTransform = None

# IP-related transforms
try:
    from spectragraph_transforms.email.to_domains import EmailToDomainsTransform
except Exception:
    EmailToDomainsTransform = None
try:
    from spectragraph_transforms.individual.to_domains import IndividualToDomainsTransform
except Exception:
    IndividualToDomainsTransform = None
try:
    from spectragraph_transforms.ip.to_domain import ReverseResolveTransform
except Exception:
    ReverseResolveTransform = None
try:
    from spectragraph_transforms.ip.to_infos import IpToInfosTransform
except Exception:
    IpToInfosTransform = None
try:
    from spectragraph_transforms.ip.to_asn import IpToAsnTransform
except Exception:
    IpToAsnTransform = None

# ASN-related transforms
try:
    from spectragraph_transforms.asn.to_cidrs import AsnToCidrsTransform
except Exception:
    AsnToCidrsTransform = None

# CIDR-related transforms
try:
    from spectragraph_transforms.cidr.to_ips import CidrToIpsTransform
except Exception:
    CidrToIpsTransform = None

# Social media transforms
try:
    from spectragraph_transforms.organization.to_domains import OrgToDomainsTransform
except Exception:
    OrgToDomainsTransform = None
try:
    from spectragraph_transforms.social.to_maigret import MaigretTransform
except Exception:
    MaigretTransform = None

# Organization-related transforms
try:
    from spectragraph_transforms.organization.to_asn import OrgToAsnTransform
except Exception:
    OrgToAsnTransform = None
try:
    from spectragraph_transforms.organization.to_infos import OrgToInfosTransform
except Exception:
    OrgToInfosTransform = None

# Cryptocurrency transforms
try:
    from spectragraph_transforms.crypto.to_transactions import (
        CryptoWalletAddressToTransactions,
    )
except Exception:
    CryptoWalletAddressToTransactions = None
try:
    from spectragraph_transforms.crypto.to_nfts import CryptoWalletAddressToNFTs
except Exception:
    CryptoWalletAddressToNFTs = None

# Website-related transforms
try:
    from spectragraph_transforms.website.to_crawler import WebsiteToCrawler
except Exception:
    WebsiteToCrawler = None
try:
    from spectragraph_transforms.website.to_links import WebsiteToLinks
except Exception:
    WebsiteToLinks = None
try:
    from spectragraph_transforms.website.to_domain import WebsiteToDomainTransform
except Exception:
    WebsiteToDomainTransform = None
try:
    from spectragraph_transforms.website.to_text import WebsiteToText
except Exception:
    WebsiteToText = None
try:
    from spectragraph_transforms.website.to_webtrackers import WebsiteToWebtrackersTransform
except Exception:
    WebsiteToWebtrackersTransform = None

# Email-related transforms
try:
    from spectragraph_transforms.email.to_gravatar import EmailToGravatarTransform
except Exception:
    EmailToGravatarTransform = None
try:
    from spectragraph_transforms.email.to_leaks import EmailToBreachesTransform
except Exception:
    EmailToBreachesTransform = None

# Phone-related transforms
try:
    from spectragraph_transforms.phone.to_leaks import PhoneToBreachesTransform
except Exception:
    PhoneToBreachesTransform = None

# Individual-related transforms
try:
    from spectragraph_transforms.individual.to_org import IndividualToOrgTransform
except Exception:
    IndividualToOrgTransform = None

# Integration transforms
try:
    from spectragraph_transforms.n8n.connector import N8nConnector
except Exception:
    N8nConnector = None


class TransformRegistry:

    _transforms: Dict[str, Type[Transform]] = {}

    @classmethod
    def register(cls, transform_class: Type[Transform]) -> None:
        cls._transforms[transform_class.name()] = transform_class

    @classmethod
    def transform_exists(cls, name: str) -> bool:
        return name in cls._transforms

    @classmethod
    def get_transform(
        cls, name: str, sketch_id: str, scan_id: str, **kwargs
    ) -> Transform:
        if name not in cls._transforms:
            raise Exception(f"Transform '{name}' not found")
        return cls._transforms[name](sketch_id=sketch_id, scan_id=scan_id, **kwargs)

    @classmethod
    def _create_transform_metadata(cls, transform: Type[Transform]) -> Dict[str, str]:
        """Helper method to create transform metadata dictionary."""
        return {
            "class_name": transform.__name__,
            "name": transform.name(),
            "module": transform.__module__,
            "description": transform.__doc__,
            "documentation": inspect.cleandoc(transform.documentation()),
            "category": transform.category(),
            "inputs": transform.input_schema(),
            "outputs": transform.output_schema(),
            "params": {},
            "params_schema": transform.get_params_schema(),
            "required_params": transform.required_params(),
            "icon": transform.icon(),
        }

    @classmethod
    def list(
        cls, exclude: Optional[List[str]] = None, wobbly_type: Optional[bool] = False
    ) -> List[Dict[str, Any]]:
        if exclude is None:
            exclude = []
        return [
            {
                **cls._create_transform_metadata(transform),
                "wobblyType": wobbly_type,
            }
            for transform in cls._transforms.values()
            if transform.name() not in exclude
        ]

    @classmethod
    def list_by_categories(cls) -> Dict[str, List[Dict[str, str]]]:
        transforms_by_category = {}
        for _, transform in cls._transforms.items():
            category = transform.category()
            if category not in transforms_by_category:
                transforms_by_category[category] = []
            transforms_by_category[category].append(
                cls._create_transform_metadata(transform)
            )
        return transforms_by_category

    @classmethod
    def list_by_input_type(
        cls, input_type: str, exclude: Optional[List[str]] = []
    ) -> List[Dict[str, str]]:
        input_type_lower = input_type.lower()

        if input_type_lower == "any":
            return [
                cls._create_transform_metadata(transform)
                for transform in cls._transforms.values()
                if transform.name() not in exclude
            ]

        return [
            cls._create_transform_metadata(transform)
            for transform in cls._transforms.values()
            if transform.input_schema()["type"].lower() in ["any", input_type_lower]
            and transform.name() not in exclude
        ]


# Register all transforms

# Domain-related transforms
if ReverseResolveTransform is not None:
    TransformRegistry.register(ReverseResolveTransform)
if ResolveTransform is not None:
    TransformRegistry.register(ResolveTransform)
if SubdomainTransform is not None:
    TransformRegistry.register(SubdomainTransform)
if WhoisTransform is not None:
    TransformRegistry.register(WhoisTransform)
if DomainToWebsiteTransform is not None:
    TransformRegistry.register(DomainToWebsiteTransform)
if DomainToRootDomain is not None:
    TransformRegistry.register(DomainToRootDomain)
if DomainToAsnTransform is not None:
    TransformRegistry.register(DomainToAsnTransform)
if DomainToHistoryTransform is not None:
    TransformRegistry.register(DomainToHistoryTransform)

# IP-related transforms
if IpToInfosTransform is not None:
    TransformRegistry.register(IpToInfosTransform)
if IpToAsnTransform is not None:
    TransformRegistry.register(IpToAsnTransform)

# ASN-related transforms
if AsnToCidrsTransform is not None:
    TransformRegistry.register(AsnToCidrsTransform)

# CIDR-related transforms
if CidrToIpsTransform is not None:
    TransformRegistry.register(CidrToIpsTransform)

# Social media transforms
if MaigretTransform is not None:
    TransformRegistry.register(MaigretTransform)

# Organization-related transforms
if OrgToAsnTransform is not None:
    TransformRegistry.register(OrgToAsnTransform)
if OrgToInfosTransform is not None:
    TransformRegistry.register(OrgToInfosTransform)
if OrgToDomainsTransform is not None:
    TransformRegistry.register(OrgToDomainsTransform)
# Cryptocurrency transforms
if CryptoWalletAddressToTransactions is not None:
    TransformRegistry.register(CryptoWalletAddressToTransactions)
if CryptoWalletAddressToNFTs is not None:
    TransformRegistry.register(CryptoWalletAddressToNFTs)

# Website-related transforms
if WebsiteToCrawler is not None:
    TransformRegistry.register(WebsiteToCrawler)
if WebsiteToLinks is not None:
    TransformRegistry.register(WebsiteToLinks)
if WebsiteToDomainTransform is not None:
    TransformRegistry.register(WebsiteToDomainTransform)
if WebsiteToWebtrackersTransform is not None:
    TransformRegistry.register(WebsiteToWebtrackersTransform)
if WebsiteToText is not None:
    TransformRegistry.register(WebsiteToText)

# Email-related transforms
if EmailToGravatarTransform is not None:
    TransformRegistry.register(EmailToGravatarTransform)
if EmailToBreachesTransform is not None:
    TransformRegistry.register(EmailToBreachesTransform)
if EmailToDomainsTransform is not None:
    TransformRegistry.register(EmailToDomainsTransform)

# Phone-related transforms
if PhoneToBreachesTransform is not None:
    TransformRegistry.register(PhoneToBreachesTransform)

# Individual-related transforms
if IndividualToOrgTransform is not None:
    TransformRegistry.register(IndividualToOrgTransform)
if IndividualToDomainsTransform is not None:
    TransformRegistry.register(IndividualToDomainsTransform)

# Integration transforms
if N8nConnector is not None:
    TransformRegistry.register(N8nConnector)
