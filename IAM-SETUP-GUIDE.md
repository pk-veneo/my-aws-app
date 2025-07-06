# IAM Setup Guide for Training Roster Automation

This guide will help you set up the required IAM roles and policies to fix the CloudFormation deployment issues.

## 🔧 Required IAM Setup

### 1. Create CloudFormation Execution Role

First, create the CloudFormation execution role with the trust policy:

```bash
# Create the role with trust policy
aws iam create-role \
  --role-name TrainingRosterCloudFormationRole \
  --assume-role-policy-document file://cloudformation-execution-role.json \
  --description "CloudFormation execution role for Training Roster Automation"

# Attach the permissions policy
aws iam put-role-policy \
  --role-name TrainingRosterCloudFormationRole \
  --policy-name CloudFormationExecutionPolicy \
  --policy-document file://cloudformation-execution-role-policy.json
```

### 2. Create GitHub Actions Role

Create the role that GitHub Actions will assume:

```bash
# Update the trust policy with your account ID and repository
# Replace ACCOUNT_ID with your AWS account ID
# Replace OWNER/REPO_NAME with your GitHub repository (e.g., yourusername/my-aws-app)

# Create the role
aws iam create-role \
  --role-name TrainingRosterGitHubActionsRole \
  --assume-role-policy-document file://github-actions-trust-policy.json \
  --description "GitHub Actions role for Training Roster Automation"
```

### 3. Create GitHub Actions Policy

Create and attach the policy for GitHub Actions:

```bash
# Create the policy document
cat > github-actions-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::*-dev",
        "arn:aws:s3:::*-qa", 
        "arn:aws:s3:::*-prod",
        "arn:aws:s3:::*-dev/*",
        "arn:aws:s3:::*-qa/*",
        "arn:aws:s3:::*-prod/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": "arn:aws:iam::ACCOUNT_ID:role/TrainingRosterCloudFormationRole"
    }
  ]
}
EOF

# Attach the policy to the GitHub Actions role
aws iam put-role-policy \
  --role-name TrainingRosterGitHubActionsRole \
  --policy-name GitHubActionsPolicy \
  --policy-document file://github-actions-policy.json
```

### 4. Update GitHub Variables

In your GitHub repository, set these variables:

- `AWS_ACCOUNT_ID`: Your AWS account ID (898465023829)
- `AWS_ROLE`: `TrainingRosterGitHubActionsRole`
- `SAM_BUCKET`: Your base S3 bucket name (e.g., `training-roster-sam`)

### 5. Update Trust Policy

Update the `github-actions-trust-policy.json` file with your actual repository:

```json
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Federated": "arn:aws:iam::898465023829:oidc-provider/token.actions.githubusercontent.com"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringLike": {
            "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/YOUR_REPO_NAME:*"
          }
        }
      }
    ]
  }
```

Replace `YOUR_GITHUB_USERNAME/YOUR_REPO_NAME` with your actual GitHub repository.

## 🚨 Troubleshooting

### If you get "Role already exists" errors:
```bash
# Delete existing roles (be careful!)
aws iam delete-role-policy --role-name TrainingRosterCloudFormationRole --policy-name CloudFormationExecutionPolicy
aws iam delete-role --role-name TrainingRosterCloudFormationRole

aws iam delete-role-policy --role-name TrainingRosterGitHubActionsRole --policy-name GitHubActionsPolicy  
aws iam delete-role --role-name TrainingRosterGitHubActionsRole
```

### Verify the roles were created correctly:
```bash
# Check the roles exist
aws iam get-role --role-name TrainingRosterCloudFormationRole
aws iam get-role --role-name TrainingRosterGitHubActionsRole

# Check the policies are attached
aws iam list-attached-role-policies --role-name TrainingRosterCloudFormationRole
aws iam list-attached-role-policies --role-name TrainingRosterGitHubActionsRole
```

## ✅ After Setup

1. Update your GitHub repository variables
2. Push to the `dev` branch to test the deployment
3. Check the GitHub Actions logs for any remaining issues

The deployment should now work without the IAM permission errors! 