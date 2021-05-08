import {useState} from 'react'
import styles from '../styles/Register.module.css'

const register = () => {

    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    
    const handleSubmit = (e) => {
        e.preventDefault()

        var formData = new FormData()

        formData.append('username', username)
        formData.append('email', email)
        formData.append('password', password)

        fetch('http://localhost:8888/register', {
            method: "POST",
            body: formData
        })
        .then(res => console.log(res.status))
    }

    return (
        <div className={styles.formContainer}>
            <form onSubmit={e => handleSubmit(e)}>
                <h1>Registrieren</h1>
                
                <label htmlFor='username'>Nutzername</label><br />
                <input className='txt-input' name='username' type='text' value={username} onChange={e => setUsername(e.target.value)} /><br />

                <label htmlFor="email">E-Mail</label><br />
                <input className='txt-input' name='email' type='email' value={email} onChange={e => setEmail(e.target.value)} /><br />

                <label htmlFor="password">Passwort</label><br />
                <input className='txt-input' name='password' type='password' value={password} onChange={e => setPassword(e.target.value)}/><br />

                <input type='submit' value='Registrieren' />
            </form>
        </div>
    )
}

export default register
