#!/usr/bin/env bash
# Deploy the advin.io home page: CloudFormation stack, then site files, then
# CDN invalidation, then a smoke check. Runs in CI via an OIDC-assumed role;
# CFN_ROLE_ARN must point at the stack's CloudFormation service role.
set -euo pipefail

STACK_NAME="${STACK_NAME:-advin-home}"
AWS_REGION="${AWS_REGION:-us-east-1}"
DOMAIN_NAME="${DOMAIN_NAME:-advin.io}"
: "${CFN_ROLE_ARN:?set CFN_ROLE_ARN to the CloudFormation service role arn}"

echo "==> Deploying stack ${STACK_NAME}"
aws cloudformation deploy \
  --region "${AWS_REGION}" \
  --stack-name "${STACK_NAME}" \
  --template-file deploy/template.yaml \
  --role-arn "${CFN_ROLE_ARN}" \
  --no-fail-on-empty-changeset

outputs=$(aws cloudformation describe-stacks \
  --region "${AWS_REGION}" --stack-name "${STACK_NAME}" \
  --query 'Stacks[0].Outputs' --output json)
bucket=$(echo "${outputs}" | python3 -c 'import json,sys; o=json.load(sys.stdin); print(next(x["OutputValue"] for x in o if x["OutputKey"]=="SiteBucketName"))')
dist_id=$(echo "${outputs}" | python3 -c 'import json,sys; o=json.load(sys.stdin); print(next(x["OutputValue"] for x in o if x["OutputKey"]=="DistributionId"))')

echo "==> Uploading site files to s3://${bucket}"
for page in index.html privacy.html terms.html sms.html; do
  aws s3 cp "${page}" "s3://${bucket}/${page}" \
    --region "${AWS_REGION}" \
    --content-type "text/html; charset=utf-8" \
    --cache-control "public, max-age=300"
done

echo "==> Invalidating distribution ${dist_id}"
invalidation=$(aws cloudfront create-invalidation \
  --distribution-id "${dist_id}" --paths "/*" \
  --query 'Invalidation.Id' --output text)
aws cloudfront wait invalidation-completed \
  --distribution-id "${dist_id}" --id "${invalidation}"

echo "==> Smoke: https://${DOMAIN_NAME}"
for i in $(seq 1 12); do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "https://${DOMAIN_NAME}/" || true)
  if [ "${code}" = "200" ]; then
    echo "smoke OK (${code})"
    exit 0
  fi
  echo "attempt ${i}: got ${code}, retrying in 20s (DNS/CDN may still be propagating)"
  sleep 20
done
echo "smoke FAILED: https://${DOMAIN_NAME}/ never returned 200" >&2
exit 1
