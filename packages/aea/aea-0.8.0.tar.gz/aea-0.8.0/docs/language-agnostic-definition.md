An Autonomous Economic Agent is, in technical terms, defined by the following characteristics:

<ul>
<li> It MUST be capable of receiving and sending `Envelopes` which satisfy the following <a href="https://developers.google.com/protocol-buffers" target="_blank">protobuf</a> schema:

``` proto
syntax = "proto3";

package fetch.aea;

message Envelope{
    string to = 1;
    string sender = 2;
    string protocol_id = 3;
    bytes message = 4;
    string uri = 5;
}
```

The format for the above fields, except `message`, is specified below.

<ul>
<li>to and sender: an address derived from the private key of a <a href="https://en.bitcoin.it/wiki/Secp256k1" target="_blank">secp256k1</a>-compatible elliptic curve</li>
<li>protocol_id: this must match a defined  <a href="https://docs.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference" target="_blank">regular expression</a> (see below)
<li>bytes: a bytes string representing a serialized message in the specified  <a href="../protocol">protocol</a></li>
<li>URI: <a href="https://tools.ietf.org/html/rfc3986" target="_blank">this syntax</a></li>
</ul>
</li>

<li> It MUST implement each protocol's message with the required meta-fields:

``` proto

    message DialogueMessage {
        int32 message_id = 1;
        string dialogue_starter_reference = 2;
        string dialogue_responder_reference = 3;
        int32 target = 4;
        bytes content = 5;
    }
```
 where `content` is replaced with the protocol specific content (see <a href="../protocol-generator">here</a> for details).
</li>

<li> It MUST implement protocols according to their specification (see <a href="../protocol-generator">here</a> for details).

<div class="admonition note">
  <p class="admonition-title">Note</p>
  <p>This section is incomplete, and will be updated soon!</p>
</div>
</li>
<li> It SHOULD implement the `fetchai/default:0.10.0` protocol which satisfies the following protobuf schema:

``` proto
syntax = "proto3";

package fetch.aea.Default;

message DefaultMessage{

    // Custom Types
    message ErrorCode{
        enum ErrorCodeEnum {
            UNSUPPORTED_PROTOCOL = 0;
            DECODING_ERROR = 1;
            INVALID_MESSAGE = 2;
            UNSUPPORTED_SKILL = 3;
            INVALID_DIALOGUE = 4;
          }
        ErrorCodeEnum error_code = 1;
    }


    // Performatives and contents
    message Bytes_Performative{
        bytes content = 1;
    }

    message Error_Performative{
        ErrorCode error_code = 1;
        string error_msg = 2;
        map<string, bytes> error_data = 3;
    }


    oneof performative{
        Bytes_Performative bytes = 5;
        Error_Performative error = 6;
    }
}
```
</li>
<li> The protocol id MUST match the following regular expression: ^[a-zA-Z0-9_]*/[a-zA-Z_][a-zA-Z0-9_]*:(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$</li>
<li> It is recommended that it processes `Envelopes` asynchronously. Note, the specification regarding the processing of messages does not impose any particular implementation, and the AEA can be designed to process envelopes either synchronously and asynchronously. However, asynchronous message handling enables the agent to be more responsive and scalable in maintaining many concurrent dialogues with its peers.
</li>
<li> It MUST have an identity in the form of, at a minimum, an address derived from a public key and its associated private key (where the eliptic curve must be of type <a href="https://en.bitcoin.it/wiki/Secp256k1" target="_blank">SECP256k1</a>).
</li>
<li> It SHOULD implement handling of errors using the `fetchai/default:0.10.0` protocol. The protobuf schema is given above.
</li>
<li> It MUST implement the following principles when handling messages:
<ul>
<li> It MUST ALWAYS handle incoming envelopes/messages and NEVER raise an exception. This ensures another AEA cannot cause the agent to fail by sending a malicious envelope/message.</li>
<li> It MUST NEVER handle outgoing messages and ALWAYS raise an exception if this rule is violated, as this would imply that the handler is resolving a bug in the implementation.</li>
</ul>
</li>
</ul>
<div class="admonition note">
  <p class="admonition-title">Note</p>
  <p>Additional constraints will be added soon!</p>
</div>
