const express = require('express');
const multer = require('multer');
const path = require('path');
const { spawn } = require('child_process');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.static('public'));

// アップロード設定
const upload = multer({ dest: 'uploads/' });

// ファイルアップロードと実行エンドポイント
app.post('/run', upload.single('exe'), (req, res) => {
  const exePath = path.resolve(req.file.path);
  const wineArgs = [exePath];

  const wine = spawn('wine', wineArgs);
  let output = '';

  wine.stdout.on('data', data => {
    output += data.toString();
  });
  wine.stderr.on('data', data => {
    output += data.toString();
  });
  wine.on('close', code => {
    res.json({ exitCode: code, output });
  });
});

// サーバ起動
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
