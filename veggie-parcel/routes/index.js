var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Veggie Parcel' });
});

/* GET orders */
router.get('/orders', function (req, res, next) {
  res.render('orders', { title: 'Veggie Parcel' });
})

router.get('/signup', function (req, res, next) {
  res.render('signup', { title: 'Veggie Parcel' });
})

module.exports = router;
