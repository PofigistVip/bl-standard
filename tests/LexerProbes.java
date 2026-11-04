import org.zenframework.z8.compiler.core.IToken;
import org.zenframework.z8.compiler.parser.grammar.lexer.Lexer;
import org.zenframework.z8.compiler.parser.grammar.lexer.token.*;

/** Direct checks of the current Z8 lexer, without the parser or runtime. */
public class LexerProbes {
    private static int checks;

    private static Lexer lexer(String source) {
        Lexer lexer = new Lexer();
        lexer.setSource(source.toCharArray());
        return lexer;
    }

    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
        checks++;
    }

    private static void error(String source, String part) {
        try {
            Lexer l = lexer(source);
            while (l.nextToken().getId() != IToken.Nothing) { }
            throw new AssertionError("Expected lexer error: " + source);
        } catch (TokenException e) {
            check(e.getMessage() != null && e.getMessage().contains(part),
                  "Unexpected lexer error for " + source + ": " + e.getMessage());
        }
    }

    private static void identifiers() {
        Lexer l = lexer("Привет _x abc123 native int void abstract true false");
        for (int i = 0; i < 7; i++) check(l.nextToken().getId() == IToken.Identifier, "identifier " + i);
        check(l.nextToken() instanceof BooleanToken, "true token");
        check(l.nextToken() instanceof BooleanToken, "false token");
        check(l.nextToken().getId() == IToken.Nothing, "end of identifiers");
        error("boolean", "reserved");
        error(new String(Character.toChars(0x10400)), "not allowed character");
    }

    private static void commentsAndStrings() {
        Lexer l = lexer("/* outer /* inner */ end */ foo // line\n bar");
        check("foo".equals(l.nextToken().getRawText()), "nested comment");
        check("bar".equals(l.nextToken().getRawText()), "line comment");
        error("/* unterminated", "end of comment not found");
        StringToken t = (StringToken)lexer("\"a\\n\\t\\\\\\\"\"").nextToken();
        check("a\n\t\\\"".equals(t.getValue()), "escape decoding");
        check("first\nsecond".equals(((StringToken)lexer("\"first\nsecond\"").nextToken()).getValue()), "multiline string");
        error("\"\\u0041\"", "bad escape sequence");
    }

    private static void numbers() {
        check(((IntegerToken)lexer("-9223372036854775808 ").nextToken()).getValue() == Long.MIN_VALUE, "minimum signed long");
        check(((IntegerToken)lexer("+ 12 ").nextToken()).getValue() == 12, "signed token with space");
        check(((IntegerToken)lexer("0x7f ").nextToken()).getValue() == 127, "hex number");
        check(((DecimalToken)lexer(".5 ").nextToken()).getValue().toPlainString().equals("0.5"), "leading dot");
        check(((DecimalToken)lexer("1.0e+2 ").nextToken()).getValue().toPlainString().equals("1.01442"), "signed exponent implementation");
        check(((DecimalToken)lexer("1.0e-2 ").nextToken()).getValue().toPlainString().equals("1.01462"), "negative exponent implementation");
        error("1.0e2 ", "expected exponent sign");
        error("9223372036854775808 ", "For input string");
        error("(-9223372036854775808)", "For input string");
        try {
            lexer("1").nextToken();
            throw new AssertionError("Expected end-of-input lexer failure");
        } catch (ArrayIndexOutOfBoundsException e) {
            check(true, "unclosed numeric token at end of file");
        }
    }

    private static void specialLiterals() {
        check(lexer("'01/01/1000'").nextToken() instanceof DateToken, "date in year 1000");
        check(lexer("'1 12:30:20'").nextToken() instanceof DatespanToken, "datespan");
        check(lexer("'00000000-0000-0000-0000-000000000001'").nextToken() instanceof GuidToken, "guid");
        check(lexer("'1, 0xFF'").nextToken() instanceof BinaryToken, "binary");
        error("'31/02/2000'", "bad 'constant' format");
        long before = System.currentTimeMillis();
        DateToken t = (DateToken)lexer("'12:34:56'").nextToken();
        long after = System.currentTimeMillis();
        check(t.getValue().getTicks() >= before - 10000 && t.getValue().getTicks() <= after + 10000, "time-only token is compilation time");
        error("'12:3:56'", "bad 'constant' format");
    }

    public static void main(String[] args) {
        identifiers(); commentsAndStrings(); numbers(); specialLiterals();
        System.out.println("PASS: " + checks + " direct lexer checks");
    }
}
