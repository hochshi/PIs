#!/usr/bin/env node

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.join(__dirname, '..');
const readJSON = (relativePath) => JSON.parse(
  fs.readFileSync(path.join(root, relativePath), 'utf8'),
);

test('math plugin is a skill-only ChatGPT-compatible bundle', () => {
  const manifest = readJSON('.codex-plugin/plugin.json');
  assert.equal(manifest.name, 'math-ponytail');
  assert.equal(manifest.skills, './skills/');
  assert.equal(manifest.hooks, undefined);
  assert.equal(manifest.apps, undefined);
  assert.equal(manifest.mcpServers, undefined);
  assert.ok(fs.existsSync(path.join(root, 'skills/ponytail-math/SKILL.md')));
});

test('marketplace installs math plugin from this fork', () => {
  const marketplace = readJSON('.agents/plugins/marketplace.json');
  const [plugin] = marketplace.plugins;
  assert.equal(marketplace.name, 'math-ponytail');
  assert.equal(plugin.name, 'math-ponytail');
  assert.equal(plugin.source.source, 'url');
  assert.equal(plugin.source.url, 'https://github.com/hochshi/math-ponytail.git');
  assert.equal(plugin.source.ref, 'agent/math-definition-discipline');
  assert.deepEqual(plugin.policy, {
    installation: 'AVAILABLE',
    authentication: 'ON_INSTALL',
  });
});
