# Matrox NMOS Source Attributes
{:.no_toc}

This document describes additional Source attributes and their permitted values which may be used in Source resources within the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

### receiver_id
- **Name:** `urn:x-matrox:receiver_id`
- **Description:** This attributes indicates the Receiver providing the essence to the Source.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3)
- **Applicability:** 
- **Permitted Values:**
  - The UUID of a Receiver.

### layer
- **Name:** `urn:x-matrox:layer`
- **Description:** This attributes indicates the Receiver's sub-Stream providing the essence to the Source.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [Matrox Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
- **Applicability:** 
- **Permitted Values:**
  - The layer value matching a sub-Stream Constraint Set of the Receiver's Capabilities.
