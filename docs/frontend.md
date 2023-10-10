# This document describes how to configure development environment for front-end

## Prerequisites 

### npm

https://www.npmjs.com/

### Backpacktravelling back-end 

Back-end can be installed locally or on remote host. 

https://github.com/backpacktraveling/backpacktraveling/blob/main/docs/backend.md

## Installation and configuration

### Clone repository

> git clone https://github.com/backpacktraveling/backant.git

Verify
> ls backant
```
README.md	
package.json	
public
src
```

### Clone second repository

> cd backant/src<br>
> rmdir restjsonapi 

(make sure that *restjsonapi* does not exist)

> git clone https://github.com/stanislawbartkowski/restjsonapi.git

Verify
> ls restjsonapi
```
LICENSE
README.md
components
layouts
services
ts
tsr-declarations.js
```

### Build or destroy

Go to *backant* directory.

> npm install 
```
npm WARN deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprecated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort#browser_compatibility
npm WARN deprecated rollup-plugin-terser@7.0.2: This package has been deprecated and is no longer maintained. Please use @rollup/plugin-terser
npm WARN deprecated w3c-hr-time@1.0.2: Use your platform's native performance.now() and performance.timeOrigin.
npm WARN deprecated sourcemap-codec@1.4.8: Please use @jridgewell/sourcemap-codec instead
npm WARN deprecated workbox-cacheable-response@6.6.0: workbox-background-sync@6.6.0
npm WARN deprecated svgo@1.3.2: This SVGO version is no longer supported. Upgrade to v2.x.x.

added 1419 packages, and audited 1420 packages in 1m

238 packages are looking for funding
  run `npm fund` for details

9 high severity vulnerabilities

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
```

Verify 
> ls node_modules<br>
```
plenty of directories and subdirectories
```

### Configure

> vi public/DEVSERVER

This file contains URL of backpacktrevelling back-end. It is a single line text file. Below is an example of back-end installed locally and listening on port *7999*

```
http://localhost:7999
```

## Run or die

Make sure that back-end is up and running. Verify that *public/DEVSERVER* file is valid

Go to *backant* directory.

> npm start

(can take several minutes)

Enjoy<br>

http://localhost:3000





