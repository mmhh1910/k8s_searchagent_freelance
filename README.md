# k8s_searchagent_freelance

Build:

    docker build --push --platform linux/arm64 -t eu-frankfurt-1.ocir.io/frs4lzee0jfi/searchagent_freelancer:latest .

Apply to setup the cronjob searches:

    k apply -f k8s/searchagent_freelance_secrets.yaml
    k apply -f k8s/searchagent_freelance_configmaps.yaml
    k apply -f k8s/searchagent_freelance_pvc.yaml
    k apply -f k8s/searchagent_freelance_cronjobs.yaml
    
Apply to run the freelancermap tag collector once:
    
    k apply -f k8s/searchagent_collect-freelancermap.yaml



