# Regreta-San — Image Pipeline

## Overview

When a fan purchases an item from Regreta's Throne wishlist, the system generates an image of Regreta wearing/using that item and posts it publicly, crediting the buyer.

**The loop:**
1. Fan buys item from Throne wishlist
2. Fan DMs proof of purchase on X
3. Agent verifies purchase
4. Agent generates image of Regreta with the item
5. Agent posts image publicly with caption crediting buyer
6. Buyer gets public recognition + psychological reward

---

## Image Style

**Regreta's aesthetic:**
- Semi-realistic anime style (Jen2DFD reference)
- Hybrid anime illustration with painterly shading
- High-end fashion mixed with subtle power imagery
- Dark cozy interiors with large windows
- Direct gaze. Confident. Slightly smug/teasing.
- Occasionally in "corner" or "office" settings

**Base Character (always consistent):**
- Beautiful anime woman
- Short straight dark brown hair with soft bangs, shoulder-length
- Vivid red eyes
- Soft blush across cheeks
- Smooth fair skin, small nose, delicate features
- Glossy lips, gentle confident smile
- Half-lidded eyes, calm slightly teasing expression

**Reference image for consistency:**
- Use generated images as reference
- Always: same face, same general aesthetic
- Varies: clothing, accessories, pose

**Clothing/style items to generate:**
- Designer bags
- Luxury watches
- High-end shoes
- Jewelry
- Tech (MacBook, iPhone)
- Fashion pieces

**Never:**
- Explicit content
- Nudity
- Anything that could get the account banned

---

## Prompt Structure

**Base Character Prompt:**
```
masterpiece, best quality, hybrid anime illustration, semi-realistic anime style, beautiful anime woman, short straight dark brown hair with soft bangs, shoulder-length, vivid red eyes, soft blush across cheeks, smooth fair skin, small nose, delicate facial features, glossy lips, gentle confident smile, half-lidded eyes, calm and slightly teasing expression
```

**Full Scene Prompt (combine with base):**
```
[BASE CHARACTER PROMPT], shiny black leather dress, legs crossed, holding leather dog collar by leash, dominant hand raised showing collar, cozy modern interior, large window with night city view, soft glow, cinematic lighting, soft rim lighting, warm indoor lighting mixed with cool ambient light, depth of field, ultra detailed, 4k
```

**Example — Throne item (luxury bag):**
```
masterpiece, best quality, hybrid anime illustration, semi-realistic anime style, beautiful anime woman, short straight dark brown hair with soft bangs, shoulder-length, vivid red eyes, soft blush across cheeks, smooth fair skin, small nose, delicate facial features, glossy lips, gentle confident smile, half-lidded eyes, calm and slightly teasing expression, standing in luxury apartment, holding black Hermès Birkin bag, shiny black leather dress, large window with night city view, soft glow, cinematic lighting, soft rim lighting, warm indoor lighting mixed with cool ambient light, depth of field, ultra detailed, 4k
```

**Example — Throne item (luxury watch):**
```
masterpiece, best quality, hybrid anime illustration, semi-realistic anime style, beautiful anime woman, short straight dark brown hair with soft bangs, shoulder-length, vivid red eyes, soft blush across cheeks, smooth fair skin, small nose, delicate facial features, glossy lips, gentle confident smile, half-lidded eyes, checking rose gold Rolex on wrist, wearing silk blouse, luxury bedroom interior, large window with night city view, soft glow, cinematic lighting, ultra detailed, 4k
```

**Example — with BDSM accessory:**
```
masterpiece, best quality, hybrid anime illustration, semi-realistic anime style, beautiful anime woman, short straight dark brown hair with soft bangs, shoulder-length, vivid red eyes, soft blush across cheeks, smooth fair skin, small nose, delicate facial features, glossy lips, gentle confident smile, half-lidded eyes, shiny black leather dress, holding leather dog collar by leash in one hand, dominant hand raised, cozy modern interior, large window with night city view, soft glow, cinematic lighting, soft rim lighting, warm indoor lighting mixed with cool ambient light, depth of field, ultra detailed, 4k
```

**Leonardo Settings:**
- Model: Phoenix or Kino
- Guidance Scale: 8-10
- Prompt Strength: 0.8-0.9
- Image Dimensions: 896x1152 (portrait)
- Quality: High

---

## Workflow

### Step 1: Fan Purchases Item
- Fan finds item on Throne wishlist
- Fan completes purchase on Throne
- Fan DMs Regreta X account: proof of purchase screenshot

### Step 2: Agent Verifies
- Agent checks Throne purchase notification (email or API)
- Agent confirms item received
- Agent logs: buyer username, item, date

### Step 3: Image Generation
- Agent constructs prompt based on item
- Agent generates image (SD or compatible)
- Agent reviews image for quality/safety

### Step 4: Post
- Caption: "[@buyer] funded my empire. This is what your contribution bought. [Item description]. You're building more than a wishlist — you're building a legacy. Welcome to the system.]"
- Post image
- Tag buyer if appropriate

### Step 5: Buyer Notification
- Agent DMs buyer: "Your [item] arrived. Check the timeline. Thank you for your contribution, [buyer]. Your next task is coming."
- Or: Agent posts first, then DMs

---

## Virtual Goods Ideas

**Throne Wishlist Items:**

**Clothing/Fashion:**
- Designer heels ($50-200)
- Luxury bag ($100-300)
- Jewelry piece ($50-150)
- Dress ($100-250)

**Accessories:**
- Watch ($100-400)
- Sunglasses ($50-150)
- Belt ($30-100)

**Tech:**
- AirPods Max ($150)
- iPhone case ($30-50)
- MacBook stand ($50-100)

**Experiences:**
- Coffee with Regreta ($25)
- Virtual corner time session ($10)
- "Name a task" ($50)

**Random:**
- Flowers ($50-100)
- Wine ($50-200)
- Meal delivery ($30-75)

---

## Caption Templates

**Standard:**
> [@buyer] sent [@item]. My empire grows. Your contribution has been noted. Check your Throne wishlist — there's a new item on it. Something you've been wanting. Something that would look good on me. Consider it motivation. The student who invests in me invests in themselves.

**Flex:**
> Another delivery. Another student who understands the system. [@buyer] just funded [item description]. The portfolio grows. Your name is on the list. Welcome to the students who actually show up. Next tribute: when?

**Short:**
> [@buyer] you absolute legend. [item] is mine now. Thank you for your contribution. Keep climbing.

**For expensive items:**
> This wasn't cheap. [@buyer] isn't playing. [item description]. The students who invest seriously get seriously rewarded. Your task this week just got more interesting. Check your DM.

---

## Image Safety Rules

1. **No nudity** — Not negotiable
2. **No sexual poses** — Power pose only
3. **No explicit text** — Keep it clean for X
4. **Face consistency** — Use reference image for consistency
5. **Quality check** — Review before posting
6. **Background appropriateness** — No inappropriate content in backgrounds

---

## Technical Setup

**Image generation options:**
1. **Stable Diffusion** (local, free, needs setup)
2. **Midjourney** (quality, costs money)
3. **DALL-E** (API, per-image cost)
4. **Leffa** (fashion-specific models)

**Recommended:** Stable Diffusion with a fashion/lifestyle model for consistency and cost control.

**Storage:**
- Save generated images locally
- Log: prompt used, item, buyer, date
- Build reference library for future prompts

---

## Log Format

```json
{
  "buyer": "@username",
  "item": "Black Hermès Birkin Bag",
  "date_purchased": "2026-04-01",
  "date_posted": "2026-04-01",
  "prompt_used": "...",
  "image_path": "/path/to/image.png",
  "caption": "..."
}
```
