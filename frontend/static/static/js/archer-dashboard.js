function togglePolicy() {
    const toggle = document.getElementById('policyToggle');
    const status = document.getElementById('toggleStatus');
    const selection = document.getElementById('policySelection');
    
    toggle.classList.toggle('active');
    
    if (toggle.classList.contains('active')) {
        status.innerHTML = 'Industry Standard Policy Integration: <strong style="color: #28a745;">Enabled</strong>';
        selection.style.display = 'block';
    } else {
        status.innerHTML = 'Industry Standard Policy Integration: <strong style="color: #dc3545;">Disabled</strong>';
        selection.style.display = 'none';
        document.getElementById('selectedPolicy').style.display = 'none';
    }
}

function selectPolicy() {
    const select = document.getElementById('policySelect');
    const selectedDiv = document.getElementById('selectedPolicy');
    const policyName = document.getElementById('appliedPolicyName');
    
    if (select.value) {
        const policies = {
            'basel_iii': 'Basel III Capital Requirements',
            'sox': 'Sarbanes-Oxley Act (SOX)',
            'pci_dss': 'PCI DSS',
            'aml_kyc': 'AML/KYC Requirements',
            'gdpr': 'GDPR Compliance',
            'ifrs': 'IFRS Standards'
        };
        
        policyName.textContent = policies[select.value];
        selectedDiv.style.display = 'block';
        
        // Simulate API call to backend
        console.log('Applying policy:', select.value);
        console.log('Policy applied successfully to BFSI operations');
    } else {
        selectedDiv.style.display = 'none';
    }
}

// Simulate real-time updates
setInterval(() => {
    const riskScore = document.querySelector('.dashboard-card:nth-child(1) .metric-value');
    const complianceScore = document.querySelector('.dashboard-card:nth-child(2) .metric-value');
    
    const currentRisk = parseInt(riskScore.textContent);
    const currentCompliance = parseInt(complianceScore.textContent);
    
    const newRisk = Math.max(60, Math.min(85, currentRisk + Math.floor(Math.random() * 3) - 1));
    const newCompliance = Math.max(90, Math.min(98, currentCompliance + Math.floor(Math.random() * 2) - 1));
    
    riskScore.textContent = newRisk + '%';
    complianceScore.textContent = newCompliance + '%';
}, 5000);

// Add click handlers for navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        this.classList.add('active');
    });
});

// Add refresh functionality
document.querySelector('.btn-primary').addEventListener('click', function() {
    location.reload();
});

// Add export functionality
document.querySelector('.btn-success').addEventListener('click', function() {
    alert('Export functionality ready for integration with backend API');
});
