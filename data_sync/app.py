import networkwhisper, sync, sys, threading, time

# XXX: Ugly constants, should be elsewhere
SETTINGS = {
    'a': {
        'keypair': "0x57083392b29bdf24512c93cfdf45d38c87d9d882da3918c59f4406445ea976a4",
        'pubkey': "0x04d94a1a01872b598c7cdc5aca2358d35eb91cd8a91eaea8da277451bb71d45c0d1eb87a31ea04e32f537e90165c870b3e115a12438c754d507ac75bddd6ecacd5",
        'friend' : "0x04ff921ddf78b5ed4537402f59a150caf9d96a83f2a345a1ddf9df12e99e7778f314c9ca72e8285eb213af84f5a7b01aabb62c67e46657976ded6658e1b9e83c73" #b
        },
    'b': {
        'keypair': "0x7b5c5af9736d9f1773f2020dd0fef0bc3c8aeaf147d2bf41961e766588e086e7",
        'pubkey' : "0x04ff921ddf78b5ed4537402f59a150caf9d96a83f2a345a1ddf9df12e99e7778f314c9ca72e8285eb213af84f5a7b01aabb62c67e46657976ded6658e1b9e83c73",
        'friend': "0x04d94a1a01872b598c7cdc5aca2358d35eb91cd8a91eaea8da277451bb71d45c0d1eb87a31ea04e32f537e90165c870b3e115a12438c754d507ac75bddd6ecacd5" #a
    }
}

def tick_process(node, whisper_node):
    while True:
        #print("tick")
        # XXX: careful maybe
        whisper_node.tick()
        node.tick()
        time.sleep(0.1)

def main():

    assert len(sys.argv) > 1, "Missing node argument. Example: 'a' or 'b'"
    # Assume exists
    settings = SETTINGS[sys.argv[1]]
    keypair = settings['keypair']
    identity_pk = settings['pubkey']
    friend_pk = settings['friend']

    # Init node
    whisper_node = networkwhisper.WhisperNodeHelper(keypair)
    node = sync.Node(identity_pk, whisper_node, 'onlineDesktop', 'interactive')

    #where?
    #whisper_node.tick()

    # XXX: A bit weird? Or very weird
    node.nodes = [node]
    # XXX: Doesn't make sense, a doesn't have b info
    # XXX
    node.addPeer(friend_pk, friend_pk)
    # Clients should decide policy
    node.share(friend_pk)

    # Start background thread
    thread = threading.Thread(target=tick_process, args=[node, whisper_node])
    thread.daemon = True
    thread.start()

    while True:
        text = input("> ")
        print("You wrote", text)
        rec = sync.new_message_record(text)
        node.append_message(rec)

        node.print_sync_state()

main()

# Ok, can send message
# Now share with these other
# And allow b to run as a proc too

# so it is sending but not recving. Why is this?
# Is it resending? 2fce e.g. for b
# Is it actually trying to receive? static peers etc
# Does burstyMobile impact things? fs

# Looking at naive print I DONT see it resending,sync state is updated! what does this mean?

#hm maybe
#ok, it IS resyncing, just abit slow. TICK? ok 100ms now
# what does bursty mobile mean? lets do onlineDesktop
