# VPS Apps

Source code for apps running on the VPS at `149.28.118.25`.

## Apps

- **thestudy/** — Dashboard app (static HTML)
- **repeatly/** — Restaurant review response SaaS (Python/Streamlit)
- **regretal/** — AI findom avatar content system (docs + assets)

## Deployment

```bash
# One-time setup on VPS
git clone https://github.com/AnimahLabs/vps-apps.git /root/vps-apps

# Deploy all apps
/root/vps-apps/deploy.sh all

# Deploy single app
/root/vps-apps/deploy.sh thestudy
/root/vps-apps/deploy.sh repeatly
/root/vps-apps/deploy.sh regretal
```

## Access

- TheStudy: `http://149.28.118.25/`
- Repeatly: `http://149.28.118.25/repeatly/`
- Regreta: `http://149.28.118.25/regretal/`
