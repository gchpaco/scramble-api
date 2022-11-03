restart: deploy
	kubectl rollout restart deployment/scramble-api

deploy: image
	kubectl apply -f kubernetes/deployment.yaml

image:
	docker build -f docker/Dockerfile -t scramble-api:latest app
