import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Map;
import java.util.HashMap;


public class CCAPIExample {
	private static final String BASE_URL = "https://sandbox-api.confidentcannabis.com/v0/";
	private static final String USER_AGENT = "confidentcannabis/1.0";

	// assumes signing is disabled for this api key
	private static final String API_KEY = "f45eab90-b2ac-4b92-8603-a43d97010cd1";

	public static void main(String[] args) throws IOException {
		// https://sandbox-api.confidentcannabis.com/v0/docs/#lab-GET
		ccGet("lab");

		Map<String, String> params = new HashMap<>();
		params.put("foo", "bar");
		params.put("testparam", "testvalue");
		String paramString = getParamsString(params);

		ccPost("signingtest", paramString);
	}

	private static HttpURLConnection getCCConnection(String route) throws IOException {
		URL urlObject = new URL(BASE_URL + route);
		HttpURLConnection con = (HttpURLConnection) urlObject.openConnection();
		con.setRequestProperty("User-Agent", USER_AGENT);
		con.setRequestProperty("X-ConfidentCannabis-APIKey", API_KEY);
		return con;
	}

	// from https://github.com/eugenp/tutorials/blob/e83002ce993a03c7dca753c050ec66deead00f9b/core-java/src/main/java/com/baeldung/http/ParameterStringBuilder.java
	private static String getParamsString(Map<String, String> params) throws UnsupportedEncodingException {
		StringBuilder result = new StringBuilder();

		for (Map.Entry<String, String> entry : params.entrySet()) {
			result.append(URLEncoder.encode(entry.getKey(), "UTF-8"));
			result.append("=");
			result.append(URLEncoder.encode(entry.getValue(), "UTF-8"));
			result.append("&");
		}

		String resultString = result.toString();
		return resultString.length() > 0 ? resultString.substring(0, resultString.length() - 1) : resultString;
	}

	public static void ccGet(String route) throws IOException {
		HttpURLConnection con = getCCConnection(route);
		con.setRequestMethod("GET");

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

	// lots of inspiration from https://gist.github.com/hitenpratap/8e1f28d60c0bb11a5bca
	public static void ccPost(String route, String paramString) throws IOException {
		HttpURLConnection con = getCCConnection(route);
		con.setRequestMethod("POST");
		con.setDoOutput(true);

		OutputStreamWriter outputStreamWriter = new OutputStreamWriter(con.getOutputStream());
		outputStreamWriter.write(paramString);
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
