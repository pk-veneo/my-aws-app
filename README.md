# Training Roster Automation

A serverless AWS Lambda application for automating training roster management with GitHub Actions CI/CD pipeline.

## 🏗️ Architecture - Part 3

- **AWS Lambda Function**: Python 3.12 runtime for training roster automation
- **API Gateway**: RESTful API endpoints for roster management
- **CloudWatch**: Logging and monitoring
- **GitHub Actions**: Automated CI/CD pipeline

## 🚀 CI/CD Pipeline

### Environment Support
- **Development**: `dev` branch → DEV environment
- **Testing**: `qa` branch → QA environment  
- **Production**: `master` branch → PROD environment

### Workflow Features
- ✅ Automatic environment detection based on branch
- ✅ AWS SAM build and package
- ✅ CloudFormation deployment with parameter overrides
- ✅ OIDC authentication (no long-term AWS credentials)
- ✅ Multi-environment parameter files

## 📁 Project Structure

```
Training-roster-automation/
├── .github/
│   ├── workflows/
│   │   ├── deploy.yml              # Main CI/CD workflow
│   │   └── get-deploy-env.yml     # Environment detection
├── src/
│   ├── main.py                     # Lambda function code
│   └── requirements.txt            # Python dependencies
├── build-scripts/
│   └── install.sh                  # Dependency installation
├── template.yml                    # SAM template
└── params.dev.json                 # Development parameters
```

## 🔧 Setup Instructions

### Prerequisites
1. AWS Account with appropriate IAM roles
2. GitHub repository with secrets configured
3. S3 bucket for SAM artifacts

### Required GitHub Secrets/Variables
- `AWS_ACCOUNT_ID`: Your AWS account ID
- `AWS_ROLE`: IAM role for GitHub Actions
- `SAM_BUCKET`: Base S3 bucket name (environment will be appended automatically)
- `APP_STACK_NAME`: CloudFormation stack name
- `PARAMETER_FILE_NAME`: Parameter file name (e.g., `params.dev.json`)

### Deployment
1. Push to `dev`, `qa`, or `master` branch
2. GitHub Actions will automatically:
   - Detect environment based on branch
   - Build and package the application
   - Deploy to AWS using CloudFormation

## 📡 API Endpoints

### Health Check
- **GET** `/health` - Service health status

### Roster Management
- **GET** `/roster` - Retrieve training roster
- **POST** `/roster` - Create new training roster

## 🔒 Security Features

- **OIDC Authentication**: Secure AWS access without long-term credentials
- **IAM Role-based Access**: Least privilege permissions
- **Environment Isolation**: Separate configurations per environment
- **CloudWatch Logging**: Centralized monitoring and debugging

## 🛠️ Development

### Local Testing
```bash
# Install AWS SAM CLI
pip install aws-sam-cli

# Build locally
sam build

# Test locally
sam local invoke TrainingRosterFunction --event events/test-event.json

# Start local API
sam local start-api
```

### Adding Dependencies
Add Python packages to `requirements.txt` in the `src/` directory.

## 📊 Monitoring

- **CloudWatch Logs**: Lambda function logs
- **API Gateway**: Request/response monitoring
- **CloudFormation**: Deployment status and rollbacks

## 🚨 Troubleshooting

### Common Issues
1. **IAM Permissions**: Ensure GitHub Actions role has necessary permissions
2. **Parameter Files**: Verify parameter file exists and is valid JSON
3. **S3 Access**: Check SAM bucket permissions and existence

### Debugging
- Check GitHub Actions logs for build/deployment errors
- Review CloudWatch logs for Lambda function issues
- Verify CloudFormation stack events for deployment problems

## 📝 License

This project follows enterprise security and compliance standards.
