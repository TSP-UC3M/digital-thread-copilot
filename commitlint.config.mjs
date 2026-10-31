// Commit message rules (project rule R6): Conventional Commits 1.0.0, in English.
// https://www.conventionalcommits.org/en/v1.0.0/
export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "header-max-length": [2, "always", 72],
  },
};
