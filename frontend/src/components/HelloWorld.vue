<template>
    <div class="hello surface-300">
        <h1 class="surface-300">Welcome to MyTube</h1>
        <ul>
            <li>
                <h3> Url : </h3>
                <input type="text" v-model="url" />
            </li>
            <li>
                <h3> Mode : </h3>
                <input type="text" v-model="mode" />
            </li>
            <li>
                <h3> Quality : </h3>
                <input type="text" v-model="quality" />
            </li>
        </ul>

        <button @click="spawn_process"> create proccess</button>
    </div>
</template>

<script>
import { ref } from "vue";
//import spawn_process from "../backend/childProccess";
const { spawn } = require("child_process").spawn;

export default {
    name: "HelloWorld",
    props: {
        msg: String,
    },

    setup() {
        const url = ref("");
        const mode = ref("");
        const quality = ref("");

        //function createProccess() {
        //spawn_process([url, mode, quality]);
        //}

        const spawn_process = () => {
            // test.py( url, mode, quality )

            const argv = [
                "https://www.youtube.com/watch?v=aoMzOgiE7rY",
                "audio",
                "min",
            ];

            // const childPython = spawn('python', ['test.py', JSON.stringify(argv)]);
            const childPython = spawn("python", ["test.py", ...argv]);

            childPython.stdout.on("data", (data) => {
                console.log(`stdout: ${data}`);
            });

            childPython.stderr.on("data", (data) => {
                console.error(`stderr: ${data}`);
            });

            childPython.stdout.on("close", (exitCode) => {
                console.log(`childPython closed with crash = ${exitCode}`);
            });
        };

        return {
            url,
            mode,
            quality,
            spawn_process,
        };
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
    margin: 40px 0 0;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    display: block;
    margin: 0 10px;
}
a {
    color: #42b983;
}
</style>
