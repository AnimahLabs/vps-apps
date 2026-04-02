#!/bin/bash
# deploy.sh - Pull latest code from GitHub and restart services
# Usage: ./deploy.sh [app-name|all]
# Example: ./deploy.sh thestudy
#          ./deploy.sh all

set -e

REPO_URL="https://github.com/AnimahLabs/vps-apps.git"
WEB_ROOT="/var/www"
NGINX_CONF="/etc/nginx/sites-enabled/thestudy"

# Apps that need nginx restart after update
NGINX_APPS="thestudy repeatly regretal"
REGRETA_DIR="regreta"

log() { echo "[$(date '+%H:%M:%S')] $1"; }

pull_latest() {
    if [ -d ".git" ]; then
        git pull origin main
    else
        git clone -b main "$REPO_URL" .
    fi
}

deploy_thestudy() {
    log "Deploying TheStudy..."
    cp thestudy/TheStudy.html /var/www/thestudy/index.html
    cp thestudy/data.json /var/www/thestudy/data.json
    log "TheStudy deployed."
}

deploy_repeatly() {
    log "Deploying Repeatly..."
    mkdir -p /var/www/repeatly
    cp repeatly/app.py /var/www/repeatly/
    log "Repeatly deployed."
}

deploy_regreta() {
    log "Deploying Regreta..."
    mkdir -p /var/www/regreta
    cp -r $REGRETA_DIR/* /var/www/regreta/
    log "Regreta deployed."
}

reload_nginx() {
    log "Reloading Nginx..."
    nginx -t && systemctl reload nginx
    log "Nginx reloaded."
}

# Main
cd /root/vps-apps

if [ "$1" == "all" ]; then
    log "Pulling latest from GitHub..."
    pull_latest
    deploy_thestudy
    deploy_repeatly
    deploy_regreta
    reload_nginx
    log "All apps deployed!"
elif [ "$1" == "thestudy" ]; then
    pull_latest
    deploy_thestudy
    reload_nginx
elif [ "$1" == "repeatly" ]; then
    pull_latest
    deploy_repeatly
elif [ "$1" == "regreta" ]; then
    pull_latest
    deploy_regreta
    reload_nginx
else
    echo "Usage: $0 [thestudy|repeatly|regreta|all]"
    exit 1
fi
