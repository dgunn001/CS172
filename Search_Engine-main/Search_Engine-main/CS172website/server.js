const express = require('express');

const app = express();

const path = require('path');
const hbs = require('express-handlebars');
app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.use(express.static(path.join(__dirname, 'public')));
app.engine('hbs', hbs({extname: 'hbs', defaultLayout: 'main', layoutsDir: __dirname + '/views/layouts/'}));
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');



const { Client } = require('@elastic/elasticsearch')
const config = require('config');
const elasticConfig = config.get('elastic');

const client = new Client({
  cloud: {
    id: elasticConfig.cloudID
  },
  auth: {
    username: elasticConfig.username,
    password: elasticConfig.password
  }
})

client.info()
  .then(response => console.log("Elastic Connected"))
  .catch(error => console.error(error))




app.get('/', function (req, res) {
    res.render('home', {
        post: {
            author: 'Janith Kasun',
            image: 'https://picsum.photos/500/500',
            comments: []
        }
    });
});



app.get("/test", function (req, res) {
  const query = {
    searchTerm: req.body.search
  };
  console.log(query.searchTerm)
  client
    .search({
      index: "test1",
      body: {
        query: {
          match: {
            html: query.searchTerm
          },
        },
      },
    })
    .then((data) => {
      let hits = data.body.hits.hits;
      console.log(hits)
      //res.send.json(hits)
      return res.json(hits)
    })
    
    .catch((err) => console.log(err));
});



app.post("/example", function (req, res) {
  const query = {
    searchTerm: req.body.search
  };
  console.log(query.searchTerm)
  client
    .search({
      index: "index",
      body: {
        query: {
          match: {
            html: query.searchTerm
          },
        },
      },
    })
    .then((data) => {
      let hits = data.body.hits.hits;
      console.log(hits)
      res.json(hits)
      res.render(res.json(hits))
      
    })
    
    .catch((err) => console.log(err));
});

app.listen(8080, () => {
    console.log('The web server has started on port 8080');
});