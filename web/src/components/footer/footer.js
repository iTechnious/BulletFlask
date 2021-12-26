import React from "react";
import "./footer.css"

const Footer = ( ) => {
    return (
        <footer className="page-footer">
            <div className="container">
                <div className="row">
                <div className="col l6 s12">
                    <h5 className="white-text">Powered by BulletFlask</h5>
                    <p className="grey-text">
                        BulletFlask ist eine hochflexible Forum Software. BulletFlask ist OpenSource und unter GPL-3.0 lizensiert.
                        Das macht es jedem kostenfrei möglich, diese Software zu betreiben.
                    </p>
                </div>
                <div id="footer-links" className="col l4 offset-l2 s12">
                    <h5 className="white-text">Links</h5>
                    <ul>
                    <li><a className="grey-text text-lighten-3" href="/home/">Home</a></li>
                    <li><a className="grey-text text-lighten-3" href="/forum/">Forum</a></li>
                    <li><a className="grey-text text-lighten-3" href="/impressum/">Impressum</a></li>
                    <li><a className="grey-text text-lighten-3" href="/datenschutz/">Datenschutz</a></li>
                    </ul>
                </div>
                </div>
            </div>
            <div className="footer-copyright">
                <div className="container">
                © 2021 Sönke Klock
                <a className="grey-text text-lighten-4 right" href="https://github.com/iTechnious/BulletFlask" target="_blank" rel="noreferrer">GitHub</a>
                </div>
            </div>
        </footer>
    )
};

export default Footer;
