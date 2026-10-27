#!/usr/bin/env bash
# One-time keyless setup: lets ONLY github.com/memorialdinh/theprestige-site read Memo's Google Analytics
# and Search Console (read-only) via Workload Identity Federation. No key files are created.
P=prestige-analytics-512901
set -u
gcloud config set project $P >/dev/null 2>&1
echo "1/5 enabling APIs..."
gcloud services enable analyticsdata.googleapis.com searchconsole.googleapis.com iamcredentials.googleapis.com sts.googleapis.com iam.googleapis.com cloudresourcemanager.googleapis.com --project $P
echo "2/5 service account..."
gcloud iam service-accounts describe prestige-reader@$P.iam.gserviceaccount.com --project $P >/dev/null 2>&1 || \
  gcloud iam service-accounts create prestige-reader --display-name="Prestige reader (GitHub, read-only)" --project $P
N=$(gcloud projects describe $P --format='value(projectNumber)')
echo "3/5 identity pool..."
gcloud iam workload-identity-pools describe github --location=global --project $P >/dev/null 2>&1 || \
  gcloud iam workload-identity-pools create github --location=global --display-name=GitHub --project $P
echo "4/5 provider (only memorialdinh/theprestige-site)..."
gcloud iam workload-identity-pools providers describe theprestige-site --location=global --workload-identity-pool=github --project $P >/dev/null 2>&1 || \
  gcloud iam workload-identity-pools providers create-oidc theprestige-site --location=global --workload-identity-pool=github \
    --issuer-uri=https://token.actions.githubusercontent.com \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
    --attribute-condition="assertion.repository=='memorialdinh/theprestige-site'" --project $P
echo "5/5 allow that repo to use the service account..."
gcloud iam service-accounts add-iam-policy-binding prestige-reader@$P.iam.gserviceaccount.com --project $P \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$N/locations/global/workloadIdentityPools/github/attribute.repository/memorialdinh/theprestige-site" >/dev/null
echo
echo "DONE"
echo "PROVIDER=projects/$N/locations/global/workloadIdentityPools/github/providers/theprestige-site"
echo "SA=prestige-reader@$P.iam.gserviceaccount.com"
