package com.structurizr.command;

import java.util.Arrays;

/** Deliberately exposes no server, cloud publishing or credential commands. */
public final class DocsCli {
    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.err.println("Usage: structurizr validate|export [options]");
            System.exit(2);
        }
        AbstractCommand command = switch (args[0]) {
            case "validate" -> new ValidateCommand();
            case "export" -> new ExportCommand();
            default -> throw new IllegalArgumentException("Supported commands: validate, export");
        };
        command.run(Arrays.copyOfRange(args, 1, args.length));
    }
}
