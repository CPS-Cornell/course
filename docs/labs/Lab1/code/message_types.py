class MessageType():
    INIT   = "INIT"    # Used to initiate a handshake.
    ACK    = "ACK"     # Used for acknowledgement.
    DATA   = "DATA"    # Used for uncompressed unencrypted data.
    CMPD   = "CMPD"    # Used for compressed data.
    ENC    = "ENC"     # Used for encrypted data.
    CMPENC = "CMPENC"  # Used for compressed and encrypted data.
    PING   = "PING"    # Used for ping messages.
    ECHO   = "ECHO"    # Used for echo messages.
