import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;


public class CCAPIExample {
	private static final String BASE_URL = "https://sandbox-api.confidentcannabis.com/";
	private static final String USER_AGENT = "confidentcannabis/1.0";

	private static final String API_KEY = "a04fca7b-7f90-4253-b22b-8da3fa4e8f47";
	private static final String API_SECRET = "fffc2606-73f1-4b87-9be5-3a5a882fef56";

	public static void main(String[] args) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		// https://sandbox-api.confidentcannabis.com/v0/docs/#lab-GET
		ccGet("v0/lab");

		// https://sandbox-api.confidentcannabis.com/v0/docs/#signingtest-POST
		HashMap params = new HashMap<String, String>();
		params.put("example_field", "foo");
		ccPost("v0/signingtest", params);
	}

	private static HttpURLConnection getCCConnection(String method, String route, Map<String, String> data) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		URL urlObject = new URL(BASE_URL + route);
		HttpURLConnection con = (HttpURLConnection) urlObject.openConnection();
		con.setRequestMethod(method);
		con.setRequestProperty("User-Agent", USER_AGENT);

		// build headers and get signature
		String timestamp = getTimestampString();
		HashMap<String, String> headers = new HashMap<String, String>();
		headers.put("X-ConfidentCannabis-Timestamp", timestamp);

		String signature = generateSignature(method, route, headers, data, API_KEY, API_SECRET);

		headers.put("X-ConfidentCannabis-APIKey", API_KEY);
		headers.put("X-ConfidentCannabis-Signature", signature);
		for (Map.Entry<String, String> entry : headers.entrySet()) {
			con.setRequestProperty(entry.getKey(), entry.getValue());
		}

		return con;
	}

	// from https://github.com/eugenp/tutorials/blob/e83002ce993a03c7dca753c050ec66deead00f9b/core-java/src/main/java/com/baeldung/http/ParameterStringBuilder.java
	private static String getParamString(Map<String, String> params) throws UnsupportedEncodingException {
		StringBuilder result = new StringBuilder();

		TreeMap<String, String> sorted = new TreeMap<String, String>(params);
		for (Map.Entry<String, String> entry : sorted.entrySet()) {
			result.append(URLEncoder.encode(entry.getKey(), "UTF-8"));
			result.append("=");
			result.append(URLEncoder.encode(entry.getValue(), "UTF-8"));
			result.append("&");
		}

		String resultString = result.toString();
		return resultString.length() > 0 ? resultString.substring(0, resultString.length() - 1) : resultString;
	}

	private static String getHeaderString(TreeMap<String, String> headers) throws UnsupportedEncodingException {
		StringBuilder result = new StringBuilder();

		for (Map.Entry<String, String> entry : headers.entrySet()) {
			result.append(URLEncoder.encode(entry.getKey().toLowerCase(), "UTF-8"));
			result.append("=");
			result.append(URLEncoder.encode(entry.getValue(), "UTF-8"));
			result.append("&");
		}

		String resultString = result.toString();
		return resultString.length() > 0 ? resultString.substring(0, resultString.length() - 1) : resultString;
	}

	private static String getTimestampString() {
		Long unixTimestamp = new Date().getTime();
		String unixTimestampString = unixTimestamp.toString();
		return unixTimestampString.substring(0, 10) + "." + unixTimestampString.substring(10, 13);
	}

	private static TreeMap getPreparedHeaders(Map<String, String> headers) {
		return new TreeMap<String, String>(headers);
	}

	private static String getHeaderListString(TreeMap<String, String> preparedHeaders) {
		StringBuilder result = new StringBuilder();
		for (Map.Entry<String, String> entry : preparedHeaders.entrySet()) {
			result.append(entry.getKey().toLowerCase());
			result.append(":");
		}

		String resultString = result.toString();
		return resultString.length() > 0 ? resultString.substring(0, resultString.length() - 1) : resultString;
	}

	private static String generateSignature(
			String method, String route, Map<String, String> headers, Map<String, String> data, String apiKey, String apiSecret
			) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		// 1. create base string by combining method and route
		String baseString = method.toUpperCase() + "/" + route;

		// 2. create sorted, lowercased list of (key, value) pairs from headers
		// dictionary (must include X-ConfidentCannabis-Timestamp but not
		// X-ConfidentCannabis-APIKey or X-ConfidentCannabis-Signature)
		TreeMap preparedHeaders = getPreparedHeaders(headers);

		// 3. create url encoded param string '{{key}}={{value]}}&...'
		//     for ordered header fields, lowercased
		String headerString = getHeaderString(preparedHeaders);

		// 4. create semi-colon separated list of lowercase
		//     header keys that will be signed eg: host;x-cc-timestamp
		String headerListString = getHeaderListString(preparedHeaders);

		// 5. create sorted list of (key, value) pairs from data
		// 6. add api_key={{api_key}} to the END of the list
		// 7. create url encoded param string '{{key}}={{value}}&...'
		//     for ordered data fields
		TreeMap sortedData = new TreeMap<String, String>(data);
		String paramString;
		if (sortedData.size() > 0) {
			paramString = getParamString(sortedData) + "&api_key=" + apiKey;
		} else {
			paramString = "api_key=" + apiKey;
		}

		// 8. percent-encode (see notes below about URI Encoding) the base string
		//     from step 1
		String encodedBaseString = URLEncoder.encode(baseString);

		// 9. combine percent encoded base string, url
		//     encoded header string, header list, and url
		//     encoded parameter string with & between them
		System.out.println("Base String: " + encodedBaseString);
		System.out.println("Header String: " + headerString);
		System.out.println("Params String: " + paramString);
		String signingString = encodedBaseString + "&" + headerString + "&" + paramString;
		System.out.println("Signing String: " + signingString);

		// 10. create sha256 hmac signature from string using api_secret
		byte[] byteKey = apiSecret.getBytes("UTF-8");
		final String HMAC_SHA512 = "HmacSHA256";
		Mac sha512_HMAC = Mac.getInstance(HMAC_SHA512);
		SecretKeySpec keySpec = new SecretKeySpec(byteKey, HMAC_SHA512);
		sha512_HMAC.init(keySpec);
		byte[] macData = sha512_HMAC.doFinal(signingString.getBytes("UTF-8"));
		String rawSignature = bytesToHex(macData);
		System.out.println("rawSignature: " + rawSignature);

		// 11. prefix with signing algorithm and header list string:
		//     'CC0-HMAC-SHA256:host;x-confidentcannabis-timestamp:'
		String signature = "CC0-HMAC-SHA256:" + headerListString + ":" + rawSignature;
		System.out.println("Final Signature: " + signature);

		return signature;
	}

	// https://stackoverflow.com/a/9855338
	private final static char[] hexArray = "0123456789abcdef".toCharArray();
	public static String bytesToHex(byte[] bytes) {
		char[] hexChars = new char[bytes.length * 2];
		for ( int j = 0; j < bytes.length; j++ ) {
			int v = bytes[j] & 0xFF;
			hexChars[j * 2] = hexArray[v >>> 4];
			hexChars[j * 2 + 1] = hexArray[v & 0x0F];
		}
		return new String(hexChars);
	}

	public static void ccGet(String route) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		ccGet(route, new HashMap<String, String>());
	}

	public static void ccGet(String route, Map<String, String> params) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		HttpURLConnection con = getCCConnection("GET", route, params);

		int responseCode = con.getResponseCode();
		System.out.println("GET Response Code :: " + responseCode);

		if (responseCode == HttpURLConnection.HTTP_OK) {
			BufferedReader in = new BufferedReader(
				new InputStreamReader(con.getInputStream())
			);
			String inputLine;
			StringBuffer response = new StringBuffer();

			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}
			in.close();

			System.out.println(response.toString());
		} else {
			System.out.println("GET request failed");
		}
	}

	public static void ccPost(String route) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		ccPost(route, new HashMap<String, String>());
	}

	// lots of inspiration from https://gist.github.com/hitenpratap/8e1f28d60c0bb11a5bca
	public static void ccPost(String route, Map<String, String> params) throws IOException, InvalidKeyException, NoSuchAlgorithmException {
		HttpURLConnection con = getCCConnection("POST", route, params);
		con.setDoOutput(true);

		OutputStreamWriter outputStreamWriter = new OutputStreamWriter(con.getOutputStream());
		outputStreamWriter.write(getParamString(params));
		outputStreamWriter.flush();

		int responseCode = con.getResponseCode();
		System.out.println("POST Response Code :: " + responseCode);

		if (responseCode == HttpURLConnection.HTTP_OK) {
			BufferedReader in = new BufferedReader(
				new InputStreamReader(con.getInputStream())
			);
			String inputLine;
			StringBuffer response = new StringBuffer();

			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}
			in.close();

			System.out.println(response.toString());
		} else {
			System.out.println("POST request failed");
		}
	}
}
