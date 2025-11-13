# 3D Hand Model

## How to Add Your GLB Model

1. **Get a 3D hand model** in GLB format
2. **Name it:** `hand.glb`
3. **Place it here:** `bionic_app/static/models/hand.glb`

## Model Requirements

Your GLB model should have bone/joint names like:
- `finger1`, `finger2`, `finger3`, `finger4`, `finger5`
- `joint1`, `joint2`, `joint3`
- `thumb_joint`, `index_joint`, `middle_joint`, `ring_joint`, `pinky_joint`

## Where to Get Free 3D Hand Models

### Option 1: Sketchfab
- Visit: https://sketchfab.com/
- Search: "hand rigged glb"
- Download free models
- Make sure it's in GLB format

### Option 2: TurboSquid
- Visit: https://www.turbosquid.com/
- Search: "hand 3d model free"
- Filter by: GLB/GLTF format

### Option 3: CGTrader
- Visit: https://www.cgtrader.com/
- Search: "hand model free"
- Download GLB format

### Option 4: Create Your Own
- Use Blender (free)
- Model a simple hand
- Export as GLB with bones

## Fallback Behavior

If `hand.glb` is not found, the system will automatically create a simple geometric hand using boxes. This ensures the simulation always works!

## Testing

1. Place your `hand.glb` file here
2. Go to: http://127.0.0.1:8000/simulation-3d-advanced/
3. The model should load automatically
4. If not, check browser console for errors

## Current Status

- ✅ Folder created
- ⚠️ No GLB model yet (using fallback geometry)
- ✅ Fallback hand works perfectly

## File Structure

```
bionic_app/static/models/
├── hand.glb          ← Place your 3D model here
└── README.md         ← This file
```
