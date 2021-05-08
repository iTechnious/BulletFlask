import Navbar from '../components/Navbar'
import '../styles/globals.css'

function App({ Component, pageProps }) {
  return (
    <>
    <main>
      <Navbar />
      <Component {...pageProps} />
    </main>
    </>
  )
}

export default App
