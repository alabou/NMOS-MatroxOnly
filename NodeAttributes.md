# Matrox NMOS Node Attributes
{:.no_toc}

This document describes additional Node attributes and their permitted values which may be used in Node resources within the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

### hostnames
- **Name:** `urn:x-matrox:hostnames`
- **Description:** This attributes provides additional information about a Node's interfaces in addition to the rquired "chassis_id", "port_id", "name" attributes. It corresponds to an array of string which are the various names that can resolve to the interface IP address.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3)
- **Applicability:** 
- **Permitted Values:**
  - hostnames compliant with the DNS and mDNS protocols. A `null` value, an empty array or if the attribute is not specified all indicate that this additional information is not provided for the interface.
