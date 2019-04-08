# Hello PSS

## Swarm hello world

```
# Geth new account
geth account new
echo "0ab9f275308307188de76f82cbc08a5258b03110" >> alice.tmp

# Get rid of password prompt later
echo "" >> password.tmp

# Start swarm node
swarm --bzzaccount `cat alice.tmp`

# Test up and down
swarm up README.md > readme-ref.tmp
swarm down bzz:/`cat readme-ref.tmp` test.tmp
```

## Feeds

```
# Using human readable topic, can equally well use --topic
swarm --bzzaccount `cat alice.tmp` feed create --name "bob"
# Returns feed manifest
# 2a0ddb7d63cc4926d168697da1ad76bdad3782611c8f75bd1ce2f8b5e096b6e0

# XXX: What's the difference? Doesn't it use bzzapi and use local instance by default?
swarm --bzzaccount `cat alice.tmp` --bzzapi http://localhost:8500 feed create --name "bob"
# 2a0ddb7d63cc4926d168697da1ad76bdad3782611c8f75bd1ce2f8b5e096b6e0

# XXX: What to do with feed manifest? How get it?

# Posting to a feed using name/topic/manifest, need hex, example here
swarm --bzzaccount `cat alice.tmp` feed update --name bob 0x68656c6c6f2031

# Reading feed info 
swarm --bzzaccount `cat alice.tmp` feed info --name "bob"
# {"feed":{"topic":"0x626f620000000000000000000000000000000000000000000000000000000000","user":"0x0ab9f275308307188de76f82cbc08a5258b03110"},"epoch":{"time":1554695168,"level":24},"protocolVersion":0}

# Reading feed updates, can't with CLI but
curl 'http://localhost:8500/bzz-feed:/?user=0x0ab9f275308307188de76f82cbc08a510&name=bob'
# `hello 1` = hex above? +1

# Posting message to feed 
echo "Hello world" > message
# Need right format for hex
cat message | hexdump -v -e '/1 "%02x"' > hex-message

swarm --bzzaccount `cat alice.tmp` --password password.tmp feed update --name bob 0x`cat hex-message`

curl 'http://localhost:8500/bzz-feed:/?user=0x0ab9f275308307188de76f82cbc08a5258b03110&name=bob'
# Hello world
```

We can use `--user` to refer to another person as opposed to `bzzaccount` by default.

## PSS

First, standalone with ethereum-samples. Second, in Go script send and receive (WIP).

## Later

Simple Go CLI