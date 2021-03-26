The obfuscated javascript is basically
```js
document.forms['svgForm'].elements['svgFile'].onchange = function (evt) {
    var reader = new FileReader();
    reader.onload = function (evt) {
        const parser = new DOMParser();
        const svg = parser.parseFromString(evt.target.result, 'image/svg+xml');
        var resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
        var resultModalBody = document.getElementById('resultModalBody');
        fetch('secret.txt').then(response => response.text()).then(data => {
            encoded = getKey(svg.getElementsByTagName('path')[0].getAttribute('d'));
            if (encoded === data) {
                resultModalBody.innerText = "The logo is legit!"
                resultModal.show();
            } else {
                resultModalBody.innerText = "The logo is counterfeit!"
                resultModal.show();
            }
        });
    };
    reader.readAsText(evt.target.files[0]);
};

const getKey = (path) => {
    let key = '', completedPath = '';
    for (var i = 0; i < path.length; i++) {
        key += MD5(completedPath + path[i]).substring(0, 4);
        completedPath += path[i];
    }
    return key;
}
```
Here, the `d` attribute is taken from the path tag of the input SVG and is hashed using the `getKey` function.
So, we have to reverse the getKey function. This can be done with something like as the characters allowed in the `d` attribute are limited.:
```js
var md5 = require('md5');

const possibleChars = ['M', 'L', 'H', 'V', 'C', 'S', 'Q', 'T', 'A', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', ' ']
const crackKey = (key) => {
    let path = '';
    for (var i = 0; i < key.length; i += 4) {
        let current = key.substring(i, i + 4);
        for (var j = 0; j < possibleChars.length; j++) {
            if (md5(path + possibleChars[j]).substring(0, 4) === current) {
                path += possibleChars[j];
                break;
            }
        }
    }
    return path;
}
```
This gives the original `d` attribute, which can then be wrapped into a basic path tag in an SVG to get the SVG back.
```xml
<svg height="210" width="1000">
  <path d="M 702 75 L 700 75 L 700 2 L 705 2 L 743 73 L 745 73 L 745 2 L 748 2 L 748 75 L 742 75 L 704 4 L 702 4 L 702 75 Z M 291 75 L 262 75 L 252 65 L 253 64 L 263 73 L 290 73 L 298 66 L 298 41 L 290 34 L 256 34 L 256 2 L 298 2 L 298 4 L 258 4 L 258 31 L 291 31 L 300 41 L 300 66 L 291 75 Z M 419 75 L 389 75 L 380 66 L 380 11 L 389 2 L 419 2 L 430 12 L 428 14 L 419 4 L 389 4 L 382 12 L 382 41 L 390 31 L 419 31 L 429 41 L 429 66 L 419 75 Z M 342 75 L 337 75 L 310 2 L 313 2 L 339 73 L 341 73 L 367 2 L 369 2 L 342 75 Z M 670 75 L 649 75 L 640 66 L 640 23 L 642 23 L 642 66 L 650 73 L 669 73 L 678 63 L 678 23 L 680 23 L 680 75 L 678 75 L 678 66 L 670 75 Z M 542 75 L 513 75 L 513 73 L 541 73 L 547 67 L 547 55 L 542 50 L 518 50 L 511 43 L 511 31 L 518 23 L 545 23 L 545 25 L 519 25 L 513 31 L 513 42 L 519 47 L 542 47 L 549 54 L 549 68 L 542 75 Z M 864 94 L 862 94 L 872 71 L 870 71 L 846 23 L 848 23 L 871 68 L 873 68 L 891 23 L 894 23 L 864 94 Z M 985 94 L 975 94 L 975 92 L 985 92 L 990 86 L 990 50 L 993 47 L 990 44 L 990 8 L 985 2 L 975 2 L 975 0 L 985 0 L 992 7 L 992 43 L 995 46 L 1001 46 L 1001 48 L 995 48 L 992 51 L 992 87 L 985 94 Z M 244 94 L 233 94 L 226 87 L 226 51 L 223 48 L 217 48 L 217 46 L 223 46 L 226 43 L 226 7 L 233 0 L 244 0 L 244 2 L 234 2 L 228 8 L 228 44 L 225 47 L 228 50 L 228 86 L 234 92 L 244 92 L 244 94 Z M 140 75 L 111 75 L 102 66 L 102 32 L 111 23 L 133 23 L 141 31 L 141 36 L 139 36 L 139 31 L 133 25 L 112 25 L 104 33 L 104 65 L 112 73 L 140 73 L 140 75 Z M 2 94 L 0 94 L 0 23 L 2 23 L 2 33 L 10 23 L 31 23 L 40 32 L 40 66 L 31 75 L 10 75 L 2 66 L 2 94 Z M 192 75 L 189 75 L 189 25 L 181 25 L 181 23 L 189 23 L 189 9 L 197 2 L 209 2 L 209 4 L 198 4 L 192 10 L 192 23 L 207 23 L 207 25 L 192 25 L 192 75 Z M 615 75 L 613 75 L 613 25 L 605 25 L 605 23 L 613 23 L 613 9 L 620 2 L 632 2 L 632 4 L 621 4 L 615 10 L 615 23 L 630 23 L 630 25 L 615 25 L 615 75 Z M 178 75 L 166 75 L 158 68 L 158 25 L 150 25 L 150 23 L 158 23 L 158 8 L 161 8 L 161 23 L 176 23 L 176 25 L 161 25 L 161 67 L 167 73 L 178 73 L 178 75 Z M 927 75 L 915 75 L 907 68 L 907 25 L 899 25 L 899 23 L 907 23 L 907 8 L 910 8 L 910 23 L 925 23 L 925 25 L 910 25 L 910 67 L 916 73 L 927 73 L 927 75 Z M 950 54 L 948 54 L 948 45 L 968 26 L 968 12 L 961 4 L 941 4 L 932 14 L 930 12 L 940 2 L 961 2 L 971 11 L 971 27 L 950 46 L 950 54 Z M 815 75 L 813 75 L 813 23 L 815 23 L 815 33 L 824 23 L 841 23 L 841 25 L 825 25 L 815 36 L 815 75 Z M 382 66 L 389 73 L 419 73 L 426 66 L 426 41 L 419 34 L 391 34 L 382 44 L 382 66 Z M 2 63 L 11 73 L 30 73 L 38 66 L 38 33 L 30 25 L 11 25 L 2 36 L 2 63 Z M 495 75 L 493 75 L 493 23 L 495 23 L 495 75 Z M 94 89 L 48 89 L 48 86 L 94 86 L 94 89 Z M 483 89 L 437 89 L 437 86 L 483 86 L 483 89 Z M 602 89 L 556 89 L 556 86 L 602 86 L 602 89 Z M 804 89 L 758 89 L 758 86 L 804 86 L 804 89 Z M 950 75 L 948 75 L 948 65 L 950 65 L 950 75 Z M 495 17 L 493 17 L 493 7 L 495 7 L 495 17 Z" />
</svg>
```

![Flag](https://i.imgur.com/Fa1JcNs.png)

The flag is: **p_ctf{5V6_is_fuN_ryt?}**