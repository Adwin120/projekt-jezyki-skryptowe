import { useRef, useState } from "react";
import { CalculatorKeyboard } from "./Keyboard";
import "./Calculator.scss"
import * as Display from "./Display"

import type { Editor } from "draft-js";

export default function Calculator() {

    const editorRef = useRef<Editor>(null);
    const [inputState, setInputState] = useState(Display.createEmptyInputState);
    const [output, setOutput] = useState("");

    const evaluate = (input: string) => {
        fetch("/calculator/parse", {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: input
        })
        .then(response => response.text())
        .then(setOutput);
    }

    const handleInput = (keyValue: string) => () => {
        editorRef.current?.focus();
        setInputState(currentState => Display.typeToInput(currentState, keyValue));
    }
    const handleReturn = () => {
        editorRef.current?.focus();
        const input = inputState.getCurrentContent().getPlainText();
        evaluate(input);
        // setInputState(currentState => Display.moveOutputToInput(currentState, ""));
    }

    const handleClear = () => {
        editorRef.current?.focus();
        setInputState(Display.createEmptyInputState)
    }

    const handleBackspace = () => {
        editorRef.current?.focus();
        setInputState(currentState => Display.deleteSelection(currentState));
    }

    return (
        <div className="calculator">
            <Display.CalculatorDisplay inputState={inputState} onChange={setInputState} output={output} ref={editorRef} />
            <div>
                {/* additional user input could go here */}
                <CalculatorKeyboard
                    handleInput={handleInput}
                    handleReturn={handleReturn}
                    handleBackspace={handleBackspace}
                    handleClear={handleClear}
                />
            </div>
        </div>
    )
}
