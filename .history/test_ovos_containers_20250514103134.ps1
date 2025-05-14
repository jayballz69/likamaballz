# See AI_CODING_BASELINE_RULES.md for required practices.
<## Description: Powershell script to test ovos_messagebus and ovos containers (AI Stack)>
# Start required services in detached mode
Write-Host "Starting ovos_messagebus and ovos containers..."
docker-compose -f docker-compose.ai.yml up -d ovos_messagebus ovos

# Wait for ovos_messagebus health
Write-Host "Waiting for ovos_messagebus to become healthy..."
while ((docker inspect --format '{{.State.Health.Status}}' ovos_messagebus) -ne 'healthy') {
    Start-Sleep -Seconds 5
    Write-Host "Still waiting for ovos_messagebus..."
}
Write-Host "ovos_messagebus is healthy."

# Wait for ovos health
Write-Host "Waiting for ovos container to become healthy..."
while ((docker inspect --format '{{.State.Health.Status}}' ovos) -ne 'healthy') {
    Start-Sleep -Seconds 5
    Write-Host "Still waiting for ovos..."
}
Write-Host "ovos is healthy."

# Run Python test scripts
Write-Host "Running ovos_messagebus_test.py..."
python .\ovos_messagebus_test.py

Write-Host "Running ovos_test_connection.py..."
python .\ovos_test_connection.py

# Tear down containers
docker-compose -f docker-compose.ai.yml down
Write-Host "Test run complete. Containers stopped."
