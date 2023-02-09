exports.execute = async function () {
    const vscode = require('vscode');

    let editor = vscode.window.activeTextEditor;
    let url = await vscode.env.clipboard.readText();
    // vscode.env.clipboard.readText().then((text)=>{
    //     url = text; 
    // });
    // vscode.window.showErrorMessage(url);
    let title = url.substring(url.lastIndexOf('/') + 1);
    let markdown = `[${title}](${url})`;
    // vscode.window.showErrorMessage(markdown);
    editor.edit(editBuilder => {
        editBuilder.insert(editor.selection.active, markdown);
    });
}