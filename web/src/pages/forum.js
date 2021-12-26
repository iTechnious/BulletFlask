import React, { Component } from 'react';
import Current from '../components/content/current';
import Content from '../components/content/content';
import Footer from '../components/footer/footer';
import "../css/forum.css";

class Forum extends Component {
    state = {
        current: {},
        content: []
    }

    getData(location) {
        console.log(location);
        let api = "http://localhost:8080";
        fetch(api + "/api/content/get/?current&location="+location.toString())
        .then(res => res.json())
        .then(data => {
            this.setState({ current: data });
        })
        .catch(console.log);

        fetch(api + "/api/content/get/?location="+location.toString())
        .then(res => res.json())
        .then(data => {
            this.setState({ content: data });
        })
        .catch(console.log);
    }

    componentDidMount() {
        this.getData(0);

        setInterval(() => {
            console.log(this.state.content)
        }, 5000);
    }
    render() {
    return (
        <>
        <main>
            <Current data={ this.state.current } />
            <Content data={ this.state.content } renew={this.getData} that={this} />
        </main>
        <Footer />
        </>
    );
    }
}

export default Forum;