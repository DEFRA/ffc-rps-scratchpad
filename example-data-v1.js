const sarahsBusiness = {
  sbi: "df34234234",
  description: "A lovely farm",
  authorisedApplicantCrn: ["123432n"],
};

landParcels = [
  {
    id: "123",
    sbi: "df34234234",
    area: 10,
    landCover: "arable",
    adjacentLandParcels: ["124"],
  },
  {
    id: "124",
    sbi: "df34234234",
    area: 5,
    landCover: "water body",
    adjacentLandParcels: ["123"],
  },
];

const sarah = {
  crn: "123432n",
  name: "Sarah",
  sbi: "df34234234",
};

const actions = [
  {
    code: "CSAM2",
    description: "Winter cover crop",
    ratePerHectare: 127,
    landCoverWhitelist: ["arable"],
    stackableActionCodeAllowlist: ["CSAM1"],
    stackableActionCodeDenylist: ["CS"],
  },
];

const legacyAgreements = [
  {
    code: "CS",
    description: "Countryside Stewardship",
  },
];

const landCovers = ["arable", "water body", "woodland"];

const eligibilityRule = () => false;
