import { useState } from 'react'
import './App.css'
import { Routes, Route, Navigate } from 'react-router-dom'
import {InputBox} from './components/inputbox.jsx'

function App() {
    return (
        <Routes>
            <Route
                path="/inputbox"
                element={
                    <InputBox
                        label="Email Address"
                        type="email"
                        placeholder="Email address"
                    />
                }
            />
        </Routes>
    )
}

export default App