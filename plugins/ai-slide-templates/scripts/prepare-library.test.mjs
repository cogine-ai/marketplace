import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { prepareLibrary } from './prepare-library.mjs';

function fixture(t) {
  const root = mkdtempSync(path.join(tmpdir(), 'slide-plugin-test-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const source = path.join(root, 'source');
  mkdirSync(source);
  for (const file of ['AGENTS.md', 'INPUT_GUIDE.md', 'scripts/preview.mjs', 'scripts/validate-visual.mjs', 'templates/demo/template.html', 'templates/demo/template.json']) {
    mkdirSync(path.dirname(path.join(source, file)), { recursive: true });
    writeFileSync(path.join(source, file), 'fixture\n');
  }
  const git = (...args) => {
    const r = spawnSync('git', args, { cwd: source, encoding: 'utf8' });
    assert.equal(r.status, 0, r.stderr);
    return r.stdout.trim();
  };
  git('init', '--quiet');
  git('add', '.');
  git('-c', 'user.name=Plugin Test', '-c', 'user.email=plugin-test@example.invalid', 'commit', '--quiet', '-m', 'Fixture');
  return { root, source, cacheRoot: path.join(root, 'cache'), pin: { repository: source, commit: git('rev-parse', 'HEAD'), template_count: 1 } };
}

test('first use fetches the exact commit; reuse works with the remote removed', t => {
  const f = fixture(t);
  const first = prepareLibrary(f);
  assert.equal(first.commit, f.pin.commit);
  assert.equal(first.templateCount, 1);
  rmSync(f.source, { recursive: true });
  assert.deepEqual(prepareLibrary(f), first);
  assert.deepEqual(readdirSync(f.cacheRoot), [f.pin.commit]);
});

test('preserves tracked edits and user files rather than resetting the cache', t => {
  const f = fixture(t);
  const result = prepareLibrary(f);
  const file = path.join(result.libraryPath, 'AGENTS.md');
  writeFileSync(file, 'local edit');
  assert.throws(() => prepareLibrary(f), /local changes/);
  assert.equal(readFileSync(file, 'utf8'), 'local edit');
  writeFileSync(file, 'fixture\n');
  writeFileSync(path.join(result.libraryPath, 'my-notes.txt'), 'keep me');
  assert.throws(() => prepareLibrary(f), /local changes/);
  assert.equal(readFileSync(path.join(result.libraryPath, 'my-notes.txt'), 'utf8'), 'keep me');
});

test('failed fetch is actionable and removes only its temporary download', t => {
  const f = fixture(t);
  f.pin.repository = path.join(f.root, 'unavailable');
  mkdirSync(f.cacheRoot);
  writeFileSync(path.join(f.cacheRoot, 'keep.txt'), 'keep');
  assert.throws(() => prepareLibrary(f), /Git fetch failed/);
  assert.deepEqual(readdirSync(f.cacheRoot), ['keep.txt']);
});

test('incomplete libraries are not published as usable caches', t => {
  const f = fixture(t);
  f.pin.template_count = 2;
  assert.throws(() => prepareLibrary(f), /Expected 2 templates, found 1/);
  assert.deepEqual(readdirSync(f.cacheRoot), []);
});

test('an unrelated directory under the version path is preserved', t => {
  const f = fixture(t);
  const occupied = path.join(f.cacheRoot, f.pin.commit);
  mkdirSync(occupied, { recursive: true });
  writeFileSync(path.join(occupied, 'keep.txt'), 'keep');
  assert.throws(() => prepareLibrary(f), /Git rev-parse failed/);
  assert.equal(readFileSync(path.join(occupied, 'keep.txt'), 'utf8'), 'keep');
});

test('a cache root containing spaces and a symlink is supported', t => {
  const f = fixture(t);
  const actual = path.join(f.root, 'actual cache');
  mkdirSync(actual);
  symlinkSync(actual, f.cacheRoot, 'dir');
  assert.equal(prepareLibrary(f).templateCount, 1);
  assert.equal(prepareLibrary(f).templateCount, 1);
});

test('CLI executes through a symlinked installed path', t => {
  const f = fixture(t);
  const plugin = fileURLToPath(new URL('..', import.meta.url));
  const linked = path.join(f.root, 'installed plugin');
  symlinkSync(plugin, linked, 'dir');
  const r = spawnSync(process.execPath, [path.join(linked, 'scripts/prepare-library.mjs'), '--help'], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /Usage: node prepare-library/);
});
