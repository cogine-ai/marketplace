import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, realpathSync, renameSync, rmSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const library = JSON.parse(readFileSync(new URL('../library.json', import.meta.url), 'utf8'));

function git(args, cwd) {
  const result = spawnSync('git', args, { cwd, encoding: 'utf8', timeout: args[0] === 'fetch' ? 600_000 : 30_000, maxBuffer: 4 * 1024 * 1024, env: { ...process.env, GIT_TERMINAL_PROMPT: '0' } });
  if (result.error) throw new Error(`Git is required; ${result.error.message}`);
  if (result.status !== 0) throw new Error(`Git ${args[0]} failed: ${result.stderr.trim()}`);
  return result.stdout.trim();
}

function verify(directory, pin) {
  if (realpathSync(git(['rev-parse', '--show-toplevel'], directory)) !== realpathSync(directory) || git(['rev-parse', 'HEAD'], directory) !== pin.commit) {
    throw new Error(`Cache does not match the pinned commit: ${directory}. Use a different --cache-dir; existing files are preserved.`);
  }
  if (git(['status', '--porcelain', '--untracked-files=all'], directory)) {
    throw new Error(`Cache has local changes: ${directory}. Preserve them and use a different --cache-dir.`);
  }
  for (const file of ['AGENTS.md', 'INPUT_GUIDE.md', 'scripts/preview.mjs', 'scripts/validate-visual.mjs']) {
    if (!existsSync(path.join(directory, file))) throw new Error(`Incomplete library: missing ${file}`);
  }
  const count = readdirSync(path.join(directory, 'templates'), { withFileTypes: true })
    .filter(entry => entry.isDirectory() && ['template.html', 'template.json'].every(file => existsSync(path.join(directory, 'templates', entry.name, file)))).length;
  if (count !== pin.template_count) throw new Error(`Expected ${pin.template_count} templates, found ${count}`);
  return { libraryPath: directory, commit: pin.commit, templateCount: count };
}

export function prepareLibrary({ cacheRoot = path.join(homedir(), '.cache', 'cogine-ai', 'ai-slide-templates'), pin = library } = {}) {
  if (Number(process.versions.node.split('.')[0]) < 22) throw new Error('Node.js 22 or newer is required.');
  if (!/^[a-f0-9]{40}$/.test(pin.commit)) throw new Error('Library commit must be a full Git SHA.');
  const root = path.resolve(cacheRoot);
  mkdirSync(root, { recursive: true });
  const canonicalRoot = realpathSync(root);
  const destination = path.join(canonicalRoot, pin.commit);
  if (existsSync(destination)) return verify(destination, pin);
  const temporary = mkdtempSync(path.join(canonicalRoot, '.download-'));
  try {
    git(['init', '--quiet', temporary]);
    git(['remote', 'add', 'origin', pin.repository], temporary);
    git(['fetch', '--quiet', '--depth=1', 'origin', pin.commit], temporary);
    git(['checkout', '--quiet', '--detach', 'FETCH_HEAD'], temporary);
    verify(temporary, pin);
    try {
      renameSync(temporary, destination);
    } catch (error) {
      if (!existsSync(destination)) throw error;
      // Another first-use process may have finished the same immutable version.
    }
    return verify(destination, pin);
  } finally {
    rmSync(temporary, { recursive: true, force: true });
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const args = process.argv.slice(2);
    if (args.length === 1 && ['--help', '-h'].includes(args[0])) {
      console.log('Usage: node prepare-library.mjs [--cache-dir <directory>]\nDownloads the pinned library once; prints its verified absolute path as JSON.');
    } else {
      if (args.length && (args.length !== 2 || args[0] !== '--cache-dir' || args[1].startsWith('--'))) throw new Error('Expected --cache-dir <directory>; see --help.');
      console.log(JSON.stringify(prepareLibrary({ cacheRoot: args[1] }), null, 2));
    }
  } catch (error) {
    console.error(`Unable to prepare slide templates: ${error.message}`);
    process.exitCode = 1;
  }
}
