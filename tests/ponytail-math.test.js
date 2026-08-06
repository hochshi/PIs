#!/usr/bin/env node

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

const skill = fs.readFileSync(
  path.join(__dirname, '..', 'skills', 'ponytail-math', 'SKILL.md'),
  'utf8',
);
const prose = skill.replace(/\s+/g, ' ');

test('math skill exposes the six definition roles', () => {
  for (const role of [
    'Unnecessary definition',
    'First definition',
    'Notation declaration',
    'Reminder',
    'Local definition',
    'Legitimate redefinition',
  ]) {
    assert.match(skill, new RegExp(`\\*\\*${role}\\*\\*`));
  }
});

test('math skill rejects low-value derived aliases', () => {
  for (const invariant of [
    'Every new name or symbol must earn the indirection it creates',
    'used once, or only in the immediately following line',
    'merely an alias of an existing object, such as a rescaling or shift',
    'Here \\(M\\) is an **unnecessary definition**',
    'meaningful conventional notation',
  ]) {
    assert.ok(prose.includes(invariant), `missing definition-utility rule: ${invariant}`);
  }
});

test('math skill protects meaning while removing repetition', () => {
  for (const invariant of [
    'same meaning is already available in the current scope',
    'state the new scope or changed condition',
    'domain or codomain, quantifier, hypothesis, dependency',
    'keep both until their equivalence is established',
    'When uncertain whether a repetition is redundant, preserve it',
  ]) {
    assert.ok(prose.includes(invariant), `missing mathematical safety rule: ${invariant}`);
  }
});
