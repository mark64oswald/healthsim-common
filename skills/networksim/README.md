# NetworkSim

> Generate realistic healthcare provider networks including providers, facilities, pharmacies, and network configurations.

## What NetworkSim Does

NetworkSim is the **provider network** engine of HealthSim. It provides two capabilities:

1. **Reference Knowledge** - Explains how healthcare networks work (HMO vs PPO, pharmacy benefits, utilization management)
2. **Synthetic Generation** - Creates realistic providers, facilities, and pharmacies with valid-format NPIs and proper taxonomy codes

When other HealthSim products need provider entities (a physician for an encounter, a pharmacy for a fill, a facility for a claim), NetworkSim provides properly structured entities that match real-world patterns.

## Quick Start

**Reference/explanation:**
```
Explain HMO vs PPO network structures
What is a pharmacy benefit manager?
How does network adequacy work?
```

**Synthetic generation:**
```
Generate a cardiologist in Houston, TX
Generate an acute care hospital with 250 beds
Generate a pharmacy network for a regional health plan
```

**Integration (for other products):**
```
Generate a provider for this cardiology encounter
Generate a dispensing pharmacy for this prescription
```

See [hello-healthsim examples](../../hello-healthsim/examples/networksim-examples.md) for detailed examples.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Reference Knowledge** | Network types, plan structures, PBM operations | [reference/](reference/) |
| **Synthetic Providers** | Physicians with NPI, specialty, credentials | [synthetic/synthetic-provider.md](synthetic/synthetic-provider.md) |
| **Synthetic Facilities** | Hospitals, ASCs, SNFs with proper characteristics | [synthetic/synthetic-facility.md](synthetic/synthetic-facility.md) |
| **Synthetic Pharmacies** | Retail, specialty, mail-order with NCPDP IDs | [synthetic/synthetic-pharmacy.md](synthetic/synthetic-pharmacy.md) |
| **Network Patterns** | HMO, PPO, tiered network templates | [patterns/](patterns/) |
| **Cross-Product Integration** | Provider entities for encounters, claims, Rx | [integration/](integration/) |

## Skill Organization

### Reference Knowledge (`reference/`)
Educational content explaining healthcare network concepts:
- [network-types.md](reference/network-types.md) - HMO, PPO, EPO, POS structures
- [plan-structures.md](reference/plan-structures.md) - Network design patterns
- [pharmacy-benefit-concepts.md](reference/pharmacy-benefit-concepts.md) - Formulary, tiers, PA
- [pbm-operations.md](reference/pbm-operations.md) - PBM business model
- [utilization-management.md](reference/utilization-management.md) - PA, step therapy, UM
- [specialty-pharmacy.md](reference/specialty-pharmacy.md) - Limited distribution, hubs
- [network-adequacy.md](reference/network-adequacy.md) - Access standards

### Synthetic Generation (`synthetic/`)
Create realistic healthcare entities:
- [synthetic-provider.md](synthetic/synthetic-provider.md) - Physicians, NPPs
- [synthetic-facility.md](synthetic/synthetic-facility.md) - Hospitals, ASCs, SNFs
- [synthetic-pharmacy.md](synthetic/synthetic-pharmacy.md) - Retail, specialty, mail
- [synthetic-network.md](synthetic/synthetic-network.md) - Complete network configurations
- [synthetic-plan.md](synthetic/synthetic-plan.md) - Health plan designs
- [synthetic-pharmacy-benefit.md](synthetic/synthetic-pharmacy-benefit.md) - PBM benefit structures

### Patterns & Templates (`patterns/`)
Reusable network design patterns:
- [hmo-network-pattern.md](patterns/hmo-network-pattern.md) - Closed network with PCP gatekeeping
- [ppo-network-pattern.md](patterns/ppo-network-pattern.md) - Open access with tiered cost sharing
- [tiered-network-pattern.md](patterns/tiered-network-pattern.md) - Preferred vs standard tiers
- [pharmacy-benefit-patterns.md](patterns/pharmacy-benefit-patterns.md) - Common formulary designs
- [specialty-distribution-pattern.md](patterns/specialty-distribution-pattern.md) - Limited distribution networks

### Cross-Product Integration (`integration/`)
Generate entities for other HealthSim products:
- [provider-for-encounter.md](integration/provider-for-encounter.md) - Provider for PatientSim
- [network-for-member.md](integration/network-for-member.md) - Network for MemberSim
- [pharmacy-for-rx.md](integration/pharmacy-for-rx.md) - Pharmacy for RxMemberSim
- [benefit-for-claim.md](integration/benefit-for-claim.md) - Benefit design for claims
- [formulary-for-rx.md](integration/formulary-for-rx.md) - Formulary context for Rx

## Integration with Other Products

| Product | NetworkSim Provides | Example |
|---------|---------------------|---------|
| **PatientSim** | Attending/referring/PCP providers | Cardiologist for heart failure admission |
| **MemberSim** | Billing providers, network status | In-network vs OON adjudication |
| **RxMemberSim** | Dispensing pharmacy, formulary | Pharmacy NCPDP, tier assignment |
| **TrialSim** | Site, principal investigator | Academic medical center PI |

## NetworkSim vs NetworkSim-Local

NetworkSim has two versions:

| Aspect | NetworkSim (Public) | NetworkSim-Local (Private) |
|--------|---------------------|----------------------------|
| **Repository** | healthsim-workspace | networksim-local |
| **Purpose** | Synthetic provider generation | Real provider data lookup |
| **Data Source** | Generated on-demand | NPPES/CMS registry (9GB) |
| **NPIs** | Valid format, synthetic | Actual registered NPIs |
| **Use Case** | Demos, tutorials, testing | Research, validation |

Most users only need the public version. NetworkSim-Local is for advanced use cases requiring real provider data.

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all capabilities
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim NetworkSim Examples](../../hello-healthsim/examples/networksim-examples.md)
- [NetworkSim Dual-Version Architecture](../../docs/networksim-dual-version.md)
- [Cross-Product Integration Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#83-cross-product-integration)

---

*NetworkSim generates synthetic provider data. NPIs are valid format but not real registrations.*
