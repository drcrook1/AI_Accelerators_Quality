$resourceGroupName = "ai-quality-dev" # $RESOURCE_GROUP
$location = "eastus"
$templateParamObject = @{
    "baseName" = "aiquadev"
    "clusterAdminUserName" = "dacrook123"
    "clusterAdminUserPassword" = "D@vid!234567890" #$clusterAdminUserPassword
    "clusterName" = "cpu"
    "minNodeCount" = 0
}

Login-AzureRmAccount
Select-AzureRmSubscription -SubscriptionName "jayoung-Team Subscription"

#Create or check for existing resource group
$resourceGroup = Get-AzureRmResourceGroup -Name $resourceGroupName -ErrorAction SilentlyContinue
if(!$resourceGroup)
{
    Write-Host "Creating resource group '$resourceGroupName' in location '$location'";
    New-AzureRmResourceGroup -Name $resourceGroupName -Location $location
}
else{
    Write-Host "Using existing resource group '$resourceGroupName'";
}

#Start Actual Deployment
New-AzureRmResourceGroupDeployment -ResourceGroupName $resourceGroupName `
                                    -Mode Incremental `
                                    -TemplateFile "./arm_templates/00_ml_template.json" `
                                    -TemplateParameterObject $templateParamObject