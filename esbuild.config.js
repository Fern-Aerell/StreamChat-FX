const esbuild = require('esbuild');
const esbuildCopy = require('esbuild-plugin-copy');

esbuild.build({
  entryPoints: ['src/**/*.ts'],
  minify: true,
  platform: 'node',
  outdir: 'dist',
  format: 'cjs',
  plugins: [
    esbuildCopy.copy({
      // Menyalin file atau folder ke folder build
      assets: [
        { from: 'LICENSE', to: 'LICENSE' },
        { from: 'service.cmd', to: 'service.cmd' },
        { from: 'package.build.json', to: 'package.json' },
        { from: 'setup_environment.exe', to: 'setup_environment.exe' },
        { from: ['./clients/**/*'], to: 'clients' },
        { from: ['./examples/index.html'], to: 'examples/index.html' },
      ]
    })
  ]
}).catch(() => process.exit(1));