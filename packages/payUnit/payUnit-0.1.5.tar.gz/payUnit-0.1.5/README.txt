# PayUnit
<p align="center">
    <a href="https://github.com/noderedis/node-redis/">
        <img width="190px" src="https://static.invertase.io/assets/node_redis_logo.png" />
    </a>
    <h2 align="center">PayUnit</h2>
    <h4 align="center">An python payment sdk for MTN Mobile Money,Orange Money,Express Union and Yup transactions.</h4>
</p>



## Installation

```bash
pip install payunit
```

## Usage

#### Example

```js
from payunit import payunit

# Enter your config details as parameters
payment = payunit({
    "user_api": "Your_User_Api",
    "password_api": "Your_Password_Api",
    "api_key": "Your_User_Api_Kay",
    "return_url": "Return_Url_To_Your_Website"
})


# Spawns a new transaction process of 4000
payment.makePayment(4000)
```
