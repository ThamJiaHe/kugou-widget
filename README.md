# kugou-widget

A serverless widget to showcase Kugou user's now playing track.

## Features

- 🎵 Display currently playing track
- 🎨 Customizable SVG widget
- ⚡ Serverless deployment with Vercel
- 🔄 Real-time updates

## Project Structure

```
kugou-widget/
├── api/
│   ├── index.py           # Main API endpoint handler
│   ├── kugou_client.py    # Kugou API client
│   ├── svg_generator.py   # SVG widget generator
│   └── requirements.txt   # Python dependencies
├── vercel.json            # Vercel configuration
├── .env.example           # Environment variables example
└── README.md              # This file
```

## Usage

### Display Widget

Add this to your GitHub README or any webpage:

```markdown
![Kugou Now Playing](https://your-deployment.vercel.app?user_id=YOUR_USER_ID)
```

### Query Parameters

- `user_id` (required): Your Kugou user ID
- `width` (optional): Widget width in pixels (default: 400)
- `height` (optional): Widget height in pixels (default: 120)

### Example

```markdown
![Kugou Now Playing](https://your-deployment.vercel.app?user_id=123456&width=500&height=150)
```

## Deployment

### Deploy to Vercel

1. Fork this repository
2. Import it to [Vercel](https://vercel.com)
3. Deploy!

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/ThamJiaHe/kugou-widget.git
cd kugou-widget
```

2. Install dependencies:
```bash
pip install -r api/requirements.txt
```

3. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Test locally with Vercel CLI:
```bash
npm i -g vercel
vercel dev
```

## Configuration

See `.env.example` for available configuration options.

## API Endpoints

### GET /

Main endpoint that returns an SVG widget.

**Query Parameters:**
- `user_id`: Kugou user ID (required)
- `width`: Widget width (optional, default: 400)
- `height`: Widget height (optional, default: 120)

**Response:**
- Content-Type: `image/svg+xml`
- Cache-Control: `public, max-age=60`

## License

MIT
