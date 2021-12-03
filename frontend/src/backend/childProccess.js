const { spawn } = require("child_process");

const spawn_process = (argv = null) => {
    // test.py( url, mode, quality )

    if (!argv)
        argv = ["https://www.youtube.com/watch?v=aoMzOgiE7rY", "audio", "min"];

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

export default spawn_process;
