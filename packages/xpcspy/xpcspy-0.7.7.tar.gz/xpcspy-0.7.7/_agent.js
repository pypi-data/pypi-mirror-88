(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.outgoingXPCMessagesFunctionPointer = void 0;
const systemFunctions_1 = require("./lib/systemFunctions");
exports.outgoingXPCMessagesFunctionPointer = [
    systemFunctions_1.xpcConnectionSendMessage,
    systemFunctions_1.xpcConnectionSendMessageWithReply,
    systemFunctions_1.xpcConnectionSendMessageWithReplySync,
    systemFunctions_1.xpcConnectionSendNotification
];

},{"./lib/systemFunctions":7}],2:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.installHooks = void 0;
const types_1 = require("./lib/types");
const helpers_1 = require("./lib/helpers");
const systemFunctions_1 = require("./lib/systemFunctions");
const formatters_1 = require("./lib/formatters");
const consts_1 = require("./consts");
const parsers_1 = require("./lib/parsers");
/**
 * TODO:
 *  - Use a class for the agent, makes more sense to store `shouldParse` and so on there.
 *  - Add `bplist16` serialization.
 *  - Add option to fetch the process' name in the connection description.
 * 	- Handle peer connections more explicitly; they have no name.
 * 	- Add option to filter services by pid.
 */
function installHooks(filter, shouldParse) {
    const pointers = [];
    if (filter.type & types_1.FilterType.Outgoing) {
        pointers.push(...consts_1.outgoingXPCMessagesFunctionPointer);
    }
    if (filter.type & types_1.FilterType.Incoming) {
        pointers.push(systemFunctions_1.xpcConnectionCallEventHandler);
    }
    for (let pointer of pointers) {
        Interceptor.attach(pointer.ptr, {
            onEnter: function (args) {
                _onEnterHandler(pointer.name, args, filter.connectionNamePattern, shouldParse);
            }
        });
    }
    send({
        'type': 'agent:hooks_installed'
    });
}
exports.installHooks = installHooks;
const _onEnterHandler = function (symbol, args, connectionNamePattern, shouldParse) {
    const p_connection = new NativePointer(args[0]);
    const connectionName = systemFunctions_1.xpcConnectionGetName.call(p_connection).readCString();
    if (connectionNamePattern != '*' && !helpers_1.wildcardMatch(connectionName, connectionNamePattern)) {
        return;
    }
    const ts = Date.now(); // Resolution isn't high enough, will have to use a dict of stacks in Python
    /*
     * Send a message to the application as soon as a new function is traced,
     * then collect/parse data (connection & dict objects, etc.) and send them to the app.
     * The app then will output full invocation data in sync, using the timestamp.
    */
    send({
        type: 'agent:trace:symbol',
        message: { timestamp: ts, symbol: symbol }
    });
    let connectionDesc = helpers_1.objcObjectDebugDesc((p_connection));
    // connectionDesc = formatConnectionDescription(connectionDesc);  // This is buggy, fix it later
    const p_message = new NativePointer(args[1]);
    let messageDesc = helpers_1.objcObjectDebugDesc(p_message);
    if (shouldParse) {
        const messageType = helpers_1.objcObjectDebugDesc(systemFunctions_1.xpcGetType.call(p_message));
        if (messageType == 'OS_xpc_dictionary') {
            const parsingResult = parsers_1.parseBPListKeysRecursively(p_message);
            if (parsingResult.length > 0) {
                messageDesc = formatters_1.formatMessageDescription(messageDesc, parsingResult);
            }
        } // Parse `OS_xpc_data` as well?
    }
    send({
        type: 'agent:trace:data',
        message: {
            timestamp: ts,
            data: { conn: connectionDesc, message: messageDesc }
        }
    });
};

},{"./consts":1,"./lib/formatters":4,"./lib/helpers":5,"./lib/parsers":6,"./lib/systemFunctions":7,"./lib/types":8}],3:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const hooking_1 = require("./hooking");
rpc.exports = {
    installHooks: (filter, shouldParse) => hooking_1.installHooks(filter, shouldParse),
};

},{"./hooking":2}],4:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.formatMessageDescription = exports.formatConnectionDescription = void 0;
function formatConnectionDescription(connectionDesc) {
    var s = connectionDesc;
    s = s.replace(/{ /g, '\n{\n\t')
        .replace(/, /g, ',\n\t')
        .replace(/<connection.*/s, '')
        .replace(/}/g, '\n}');
    return s;
}
exports.formatConnectionDescription = formatConnectionDescription;
function formatMessageDescription(messageDesc, parsingResult) {
    var s = messageDesc;
    for (let result of parsingResult) {
        s = s.replace(new RegExp(`(${result.key}.*\n)`), `$1Parsed ${result.format} data for key '${result.key}': \n${result.data}\n`);
    }
    return s;
}
exports.formatMessageDescription = formatMessageDescription;

},{}],5:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.isSupportedBPListData = exports.objcObjectDebugDesc = exports.wildcardMatch = void 0;
function wildcardMatch(target, pattern) {
    /**
     * Matches a wildcard pattern, .e.g. 'com.apple.*', with `target`.
     */
    pattern = pattern.replace('*', '\.\*');
    pattern = '\^' + pattern;
    let exp = new RegExp(pattern);
    return exp.test(target);
}
exports.wildcardMatch = wildcardMatch;
function objcObjectDebugDesc(ptr) {
    return (new ObjC.Object(ptr)).toString();
}
exports.objcObjectDebugDesc = objcObjectDebugDesc;
function isSupportedBPListData(bytesPtr) {
    const magic = bytesPtr.readCString(8);
    return magic == 'bplist00' || magic == 'bplist15';
}
exports.isSupportedBPListData = isSupportedBPListData;

},{}],6:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseBPListKeysRecursively = void 0;
const helpers_1 = require("../lib/helpers");
const systemFunctions_1 = require("../lib/systemFunctions");
function parseBPListKeysRecursively(xpcDict) {
    const objType = helpers_1.objcObjectDebugDesc(systemFunctions_1.xpcGetType.call(xpcDict));
    if (objType != 'OS_xpc_dictionary') {
        throw Error("Bad object type " + objType);
    }
    const parsingResult = [];
    /**
     * See: https://developer.apple.com/documentation/xpc/1505404-xpc_dictionary_apply?language=objc
     */
    const block_impl = function (key, value) {
        const valueType = helpers_1.objcObjectDebugDesc(systemFunctions_1.xpcGetType.call(value));
        switch (valueType) {
            case 'OS_xpc_dictionary':
                parsingResult.push(...parseBPListKeysRecursively(value));
                break;
            case 'OS_xpc_data':
                const bytesPtr = systemFunctions_1.xpcDataGetBytesPtr.call(value);
                if (helpers_1.isSupportedBPListData(bytesPtr)) {
                    const length = systemFunctions_1.xpcDataGetLength.call(value);
                    const r = parseBPList(bytesPtr, length);
                    r.key = key.readCString();
                    parsingResult.push(r);
                }
                break;
            default:
                break;
        }
        return true;
    };
    const applierBlock = new ObjC.Block({
        implementation: block_impl,
        retType: 'bool',
        argTypes: ['pointer', 'pointer']
    });
    systemFunctions_1.xpcDictionaryApply.call(xpcDict, applierBlock.handle);
    return parsingResult;
}
exports.parseBPListKeysRecursively = parseBPListKeysRecursively;
function parseBPList(bytesPtr, length) {
    /**
     * Parse binary plist data after detecting its format
     */
    const bplistFmt = bytesPtr.readCString(8);
    if (bplistFmt == 'bplist15') {
        return {
            key: null,
            data: helpers_1.objcObjectDebugDesc(systemFunctions_1.__CFBinaryPlistCreate15.call(bytesPtr, length, ptr(0x0))),
            format: 'bplist15'
        };
    }
    else if (bplistFmt == 'bplist00') {
        return parseBPlist00(bytesPtr, length);
    } // Add bplist16 serialization
}
function parseBPlist00(bytesPtr, length) {
    const data = ObjC.classes.NSData.dataWithBytes_length_(bytesPtr, length);
    const format = Memory.alloc(8);
    format.writeU64(0xaaaaaaaa);
    const plist = ObjC.classes.NSPropertyListSerialization.propertyListWithData_options_format_error_(data, 0, format, ptr(0x0));
    return {
        key: null,
        data: helpers_1.objcObjectDebugDesc(plist),
        format: 'bplist00'
    };
}

},{"../lib/helpers":5,"../lib/systemFunctions":7}],7:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.__CFBinaryPlistCreate15 = exports.xpcConnectionCallEventHandler = exports.xpcConnectionSendNotification = exports.xpcConnectionSendMessageWithReplySync = exports.xpcConnectionSendMessageWithReply = exports.xpcConnectionSendMessage = exports.xpcDataGetLength = exports.xpcDataGetBytesPtr = exports.xpcGetType = exports.xpcDictionaryApply = exports.xpcConnectionGetName = void 0;
const libXPCDylib = 'libxpc.dylib';
const p_xpc_connection_get_name = Module.getExportByName(libXPCDylib, 'xpc_connection_get_name');
const p_xpc_dictionary_apply = Module.getExportByName(libXPCDylib, 'xpc_dictionary_apply');
const p_xpc_get_type = Module.getExportByName(libXPCDylib, 'xpc_get_type');
const p_xpc_data_get_bytes_ptr = Module.getExportByName(libXPCDylib, 'xpc_data_get_bytes_ptr');
const p_xpc_data_get_length = Module.getExportByName(libXPCDylib, 'xpc_data_get_length');
const p_xpc_connection_send_message = Module.getExportByName(libXPCDylib, 'xpc_connection_send_message');
const p_xpc_connection_send_message_with_reply = Module.getExportByName(libXPCDylib, 'xpc_connection_send_message_with_reply');
const p_xpc_connection_send_message_with_reply_sync = Module.getExportByName(libXPCDylib, 'xpc_connection_send_message_with_reply_sync');
const p_xpc_connection_send_notification = Module.getExportByName(libXPCDylib, 'xpc_connection_send_notification');
const p__xpc_Connection_call_event_handler = DebugSymbol.fromName('_xpc_connection_call_event_handler').address;
const p___CFBinaryPlistCreate15 = DebugSymbol.fromName('__CFBinaryPlistCreate15').address;
exports.xpcConnectionGetName = {
    name: 'xpc_connection_get_name',
    ptr: p_xpc_connection_get_name,
    call: new NativeFunction(p_xpc_connection_get_name, 'pointer', ['pointer'])
};
exports.xpcDictionaryApply = {
    name: 'xpc_dictionary_apply',
    ptr: p_xpc_dictionary_apply,
    call: new NativeFunction(p_xpc_dictionary_apply, 'pointer', ['pointer', 'pointer'])
};
exports.xpcGetType = {
    name: 'xpc_get_type',
    ptr: p_xpc_get_type,
    call: new NativeFunction(p_xpc_get_type, 'pointer', ['pointer'])
};
exports.xpcDataGetBytesPtr = {
    name: 'xpc_data_get_bytes_ptr',
    ptr: p_xpc_data_get_bytes_ptr,
    call: new NativeFunction(p_xpc_data_get_bytes_ptr, 'pointer', ['pointer'])
};
exports.xpcDataGetLength = {
    name: 'xpc_data_get_length',
    ptr: p_xpc_data_get_length,
    call: new NativeFunction(p_xpc_data_get_length, 'uint32', ['pointer'])
};
exports.xpcConnectionSendMessage = {
    name: 'xpc_connection_send_message',
    ptr: p_xpc_connection_send_message,
    call: new NativeFunction(p_xpc_connection_send_message, 'void', ['pointer', 'pointer'])
};
exports.xpcConnectionSendMessageWithReply = {
    name: 'xpc_connection_send_message_with_reply',
    ptr: p_xpc_connection_send_message_with_reply,
    call: new NativeFunction(p_xpc_connection_send_message_with_reply, 'void', ['pointer', 'pointer', 'pointer', 'pointer'])
};
exports.xpcConnectionSendMessageWithReplySync = {
    name: 'xpc_connection_send_message_with_reply_sync',
    ptr: p_xpc_connection_send_message_with_reply_sync,
    call: new NativeFunction(p_xpc_connection_send_message_with_reply_sync, 'void', ['pointer', 'pointer', 'pointer', 'pointer'])
};
exports.xpcConnectionSendNotification = {
    name: 'xpc_connection_send_notification',
    ptr: p_xpc_connection_send_notification,
    call: new NativeFunction(p_xpc_connection_send_notification, 'void', ['pointer', 'pointer'])
};
exports.xpcConnectionCallEventHandler = {
    name: '_xpc_connection_call_event_handler',
    ptr: p__xpc_Connection_call_event_handler,
    call: new NativeFunction(p__xpc_Connection_call_event_handler, 'void', ['pointer', 'pointer'])
};
exports.__CFBinaryPlistCreate15 = {
    name: '__CFBinaryPlistCreate15',
    ptr: p___CFBinaryPlistCreate15,
    call: new NativeFunction(p___CFBinaryPlistCreate15, 'pointer', ['pointer', 'uint64', 'pointer'])
};

},{}],8:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.FilterType = void 0;
var FilterType;
(function (FilterType) {
    FilterType[FilterType["Incoming"] = 1] = "Incoming";
    FilterType[FilterType["Outgoing"] = 2] = "Outgoing";
    FilterType[FilterType["All"] = 3] = "All";
})(FilterType = exports.FilterType || (exports.FilterType = {}));

},{}]},{},[3])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzcmMvY29uc3RzLnRzIiwic3JjL2hvb2tpbmcudHMiLCJzcmMvaW5kZXgudHMiLCJzcmMvbGliL2Zvcm1hdHRlcnMudHMiLCJzcmMvbGliL2hlbHBlcnMudHMiLCJzcmMvbGliL3BhcnNlcnMudHMiLCJzcmMvbGliL3N5c3RlbUZ1bmN0aW9ucy50cyIsInNyYy9saWIvdHlwZXMudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7Ozs7QUNDQSwyREFHeUU7QUFHNUQsUUFBQSxrQ0FBa0MsR0FBdUI7SUFDbEUsMENBQXdCO0lBQ3hCLG1EQUFpQztJQUNqQyx1REFBcUM7SUFDckMsK0NBQTZCO0NBQ2hDLENBQUE7Ozs7OztBQ1pELHVDQUF5QztBQUV6QywyQ0FBbUU7QUFDbkUsMkRBR2lDO0FBQ2pDLGlEQUNxRDtBQUNyRCxxQ0FBOEQ7QUFDOUQsMkNBQTJEO0FBRTNEOzs7Ozs7O0dBT0c7QUFHSCxTQUFnQixZQUFZLENBQUMsTUFBZSxFQUFFLFdBQW9CO0lBQ2pFLE1BQU0sUUFBUSxHQUF1QixFQUFFLENBQUM7SUFFeEMsSUFBSSxNQUFNLENBQUMsSUFBSSxHQUFHLGtCQUFVLENBQUMsUUFBUSxFQUFFO1FBQ3RDLFFBQVEsQ0FBQyxJQUFJLENBQUMsR0FBRywyQ0FBa0MsQ0FBQyxDQUFDO0tBQ3JEO0lBRUQsSUFBSSxNQUFNLENBQUMsSUFBSSxHQUFHLGtCQUFVLENBQUMsUUFBUSxFQUFFO1FBQ3RDLFFBQVEsQ0FBQyxJQUFJLENBQUMsK0NBQTZCLENBQUMsQ0FBQztLQUM3QztJQUVELEtBQUssSUFBSSxPQUFPLElBQUksUUFBUSxFQUFFO1FBQzdCLFdBQVcsQ0FBQyxNQUFNLENBQUMsT0FBTyxDQUFDLEdBQUcsRUFDN0I7WUFDQyxPQUFPLEVBQUUsVUFBa0MsSUFBeUI7Z0JBQ25FLGVBQWUsQ0FBQyxPQUFPLENBQUMsSUFBSSxFQUFFLElBQUksRUFBRSxNQUFNLENBQUMscUJB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
