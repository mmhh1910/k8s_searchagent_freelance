# k8s_searchagent_freelance


docker build --push --platform linux/arm64 -t eu-frankfurt-1.ocir.io/frs4lzee0jfi/searchagent_freelancer:latest .

k apply -f k8s/searchagent_freelance_secrets.yaml
k apply -f k8s/searchagent_freelance_configmaps.yaml
k apply -f k8s/searchagent_freelance_cronjobs.yaml

