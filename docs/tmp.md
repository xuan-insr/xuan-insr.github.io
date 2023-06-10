# 111

<style>
    #container {
        position: relative;
        width: 500px;
        height: 800px;
        margin: 0 auto;
    }

    #tap {
        position: absolute;
        top: 0;
        width: 100%;
    }

    #cup {
        position: absolute;
        top: 200px;
        width: 100%;
        height: 80%;
        overflow: hidden;
    }

    #cup img {
        width: 100%;
        height: 100%;
    }

    #water {
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 0;
        background-color: blue;
        transition: height 0.2s linear;
    }

    #line {
        position: absolute;
        top: 20%;
        width: 100%;
        height: 2px;
        background-color: red;
    }
</style>
<body>
    <div id="container">
        <img id="tap" src="tap.png">
        <div id="cup">
            <img src="cup.png">
            <div id="water"></div>
            <div id="line"></div>
        </div>
        <button id="btn-start">开始</button>
        <button id="btn-reset">重置</button>
        <button id="btn-show">显示结果</button>
    </div>
</body>
<script>
    var water = document.getElementById('water');
    var btnStart = document.getElementById('btn-start');
    var btnReset = document.getElementById('btn-reset');
    var btnShow = document.getElementById('btn-show');
    var waterLevel = 0;
    var timer = null;

    btnStart.onmousedown = function() {
        timer = setInterval(function() {
            if (waterLevel < 80) {
                waterLevel += 1;
                water.style.height = waterLevel + '%';
            }
        }, 100);
    }

    btnStart.onmouseup = function() {
        clearInterval(timer);
        timer = null;
    }

    btnReset.onclick = function() {
        waterLevel = 0;
        water.style.height = '0';
    }

    btnShow.onclick = function() {
        alert('水位：' + waterLevel + '%');
    }
</script>