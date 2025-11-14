# 🎵 Popular Songs Database

Ready-to-use songs with album art URLs for your Kugou widget.

## Jay Chou (周杰伦) - Most Popular Songs

### Quick Update Commands

```bash
# 晴天 (Sunny Day) - From "Ye Hui Mei" Album
python update_song.py "晴天" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"

# 告白气球 (Love Confession) - From "Jay Chou's Bedtime Stories" Album
python update_song.py "告白气球" "周杰伦" "https://imge.kugou.com/stdmusic/240/20170418/20170418173403349763.jpg"

# 青花瓷 (Blue and White Porcelain) - From "On the Run" Album
python update_song.py "青花瓷" "周杰伦" "https://imge.kugou.com/stdmusic/240/20160818/20160818112845056710.jpg"

# 稻香 (Rice Fragrance) - From "Capricorn" Album
python update_song.py "稻香" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150719/20150719205742894772.jpg"

# 七里香 (Common Jasmine Orange) - From "Common Jasmine Orange" Album
python update_song.py "七里香" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120645762966.jpg"

# 夜曲 (Nocturne) - From "November's Chopin" Album
python update_song.py "夜曲" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120644965842.jpg"

# 彩虹 (Rainbow) - From "I'm Very Busy" Album
python update_song.py "彩虹" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120649308594.jpg"

# 简单爱 (Simple Love) - From "Fantasy" Album
python update_song.py "简单爱" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120612604284.jpg"

# 以父之名 (In the Name of Father) - From "Ye Hui Mei" Album
python update_song.py "以父之名" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"

# 东风破 (East Wind Breaks) - From "Common Jasmine Orange" Album
python update_song.py "东风破" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120645762966.jpg"

# 枫 (Maple) - From "November's Chopin" Album
python update_song.py "枫" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120644965842.jpg"

# 安静 (Silence) - From "Fantasy" Album
python update_song.py "安静" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120612604284.jpg"

# 搁浅 (Stranded) - From "November's Chopin" Album
python update_song.py "搁浅" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120644965842.jpg"

# 算什么男人 (What Kind of Man) - From "The Era" Album
python update_song.py "算什么男人" "周杰伦" "https://imge.kugou.com/stdmusic/240/20111129/20111129173225181634.jpg"

# 不能说的秘密 (Secret) - From "Secret" Movie Soundtrack
python update_song.py "不能说的秘密" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120647433728.jpg"
```

## Song Data Structure (For Firebase)

If you want to add these directly to Firebase:

```json
{
  "users": {
    "YOUR_USERNAME": {
      "current_song": {
        "name": "晴天",
        "artist": "周杰伦",
        "cover": "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg",
        "updated_at": 1731575100000
      }
    }
  }
}
```

## Album Art URLs Reference

| Song | Artist | Album Cover URL |
|------|--------|-----------------|
| 晴天 | 周杰伦 | https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg |
| 告白气球 | 周杰伦 | https://imge.kugou.com/stdmusic/240/20170418/20170418173403349763.jpg |
| 青花瓷 | 周杰伦 | https://imge.kugou.com/stdmusic/240/20160818/20160818112845056710.jpg |
| 稻香 | 周杰伦 | https://imge.kugou.com/stdmusic/240/20150719/20150719205742894772.jpg |
| 七里香 | 周杰伦 | https://imge.kugou.com/stdmusic/240/20150718/20150718120645762966.jpg |
| 夜曲 | 周杰伦 | https://imge.kugou.com/stdmusic/240/20150718/20150718120644965842.jpg |
| 彩虹 | 周杰伦 | https://imge.kugou.com/stdmusic/240/20150718/20150718120649308594.jpg |
| 简单爱 | 周杰伦 | https://imge.kugou.com/stdmusic/240/20150718/20150718120612604284.jpg |

## How to Use

### Method 1: Using update_song.py Script

1. Make sure you've configured `update_song.py` with your USER_ID
2. Run any command from above
3. Check your GitHub profile to see the update

### Method 2: Manual API Call

```bash
curl -X POST https://YOUR_VERCEL_URL/update \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_USERNAME",
    "song_name": "晴天",
    "artist_name": "周杰伦",
    "cover_url": "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"
  }'
```

### Method 3: Direct Firebase Update

1. Go to Firebase Console → Realtime Database
2. Navigate to `users/YOUR_USERNAME/current_song`
3. Update the fields manually

## Finding More Album Art

To find album art for other songs:

1. **Search on Kugou:** Visit https://www.kugou.com and search for the song
2. **Inspect Image:** Right-click album art → Copy image address
3. **Use Format:** Kugou images follow pattern: `https://imge.kugou.com/stdmusic/240/YYYYMMDD/...jpg`
4. **Default Size:** Use `/240/` for widget-sized images

## Tips

- **Update frequently** - Change your widget whenever you listen to new music
- **Use emoji** - Add emoji to song names for fun: `"晴天 ☀️"`
- **Custom covers** - Use any image URL for the cover (not just Kugou)
- **Test first** - Try with demo mode: `?user_id=demo` before using your own ID

## Troubleshooting

**Widget not updating?**
- Check Firebase rules allow writes
- Verify your user_id matches in script and Firebase
- Check the API response for errors

**Image not showing?**
- Use HTTPS URLs only
- Test the image URL in browser first
- Use Kugou CDN URLs for best compatibility
