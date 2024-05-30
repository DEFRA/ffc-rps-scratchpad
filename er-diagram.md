```mermaid
erDiagram
business ||..|{ land-parcel : has
applicant }|..|{ business: applies-on-behalf-of
action ||..|{ eligibility-rule : has
land-parcel ||..O{ land-feature : has
land-parcel ||..|{ land-cover : has
land-parcel ||..O{ land-use : has
land-parcel }|..O{ action : has
action }O..O{ legacy-agreement: has-exclusion
```
