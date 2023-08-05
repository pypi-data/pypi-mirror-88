diff --git a/lilcom/lilcom.h b/lilcom/lilcom.h
index 960e067..ca4e02d 100644
--- a/lilcom/lilcom.h
+++ b/lilcom/lilcom.h
@@ -1,23 +1,24 @@
 #include <stdint.h>
 #include <sys/types.h>
 
+
+typedef void* LilcomConfigT;
+
 /**
-   Returns the number of bytes we'd need to compress a sequence with this
-   many samples and the provided bits_per_sample.
+   Returns an opaque type which defines a set of configuration values.  The type
+   will contain other values other than the ones explicitly provided, but for
+   now these will be set to some appropriate default values and are not user
+   specifiable.
+*/
+LilcomConfigT* lilcom_get_config(int samp_rate,
+                                 int num_channels,
+                                 int lpc_order,
+                                 int max_bits_per_sample,
+                                 int block_size);
 
-      @param [in] num_samples  Must be >0.  The length of the
-                      input sequence
-      @param [in] bits_per_sample  The bits per sample to be used
-                      for compression; must be in [4..8]
+void lilcom_delete_config(LilcomConfigT *config);
 
-      @return  If the inputs were valid, returns the number of
-             bytes needed to compress this sequence; this will always be >= 5,
-             since the header is 4 bytes and there must be at least one sample.
 
-             If an input was out of range, returns -1.
-*/
-ssize_t lilcom_get_num_bytes(ssize_t num_samples,
-                             int bits_per_sample);
 
 /**
    Lossily compresses 'num_samples' samples of int16 sequence data (e.g. audio
@@ -35,10 +36,6 @@ ssize_t lilcom_get_num_bytes(ssize_t num_samples,
                       Note: the header will not contain the length of the
                       sequence; the length of the byte sequence will be
                       required to work out the original `num_samples`.
-      @param [in] num_bytes  The number of bytes in the compressed output;
-                      if this not equal to
-                      `lilcom_get_num_bytes(num_samples, bits_per_sample)`,
-                      this function will return error status (1).
       @param [in] output_stride  The offset from one output sample to
                       the next.  Would normally be 1, but may have any nonzero
                       value.
@@ -75,10 +72,18 @@ ssize_t lilcom_get_num_bytes(ssize_t num_samples,
 
    This process can (approximately) be reversed by calling `lilcom_decompress`.
 */
-int lilcom_compress(const int16_t *input, ssize_t num_samples, int input_stride,
+
+/**
+int lilcom_compress_int16(const int16_t *input,
+                          ssize_t num_samples, int sample_stride,
+                          int num_channels, int channel_stride,
+                          int8_t **output,
+
                     int8_t *output, ssize_t num_bytes, int output_stride,
                     int lpc_order, int bits_per_sample,
                     int conversion_exponent);
+           TODO:  find new version
+*/
 
 /**
    Lossily compresses 'num_samples' samples of floating-point sequence data
