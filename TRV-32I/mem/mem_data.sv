module mem_data #(
    parameter B_WIDTH = 32;
    parameter MEM_SIZE = 32;
) (
    input                   clk, rst;
    input [B_WIDTH-1:0]     mem_addr;
    input                   mem_read_en, mem_write_en;
    input [(B_WIDTH/8)-1:0] write_byte_en;
    inout [B_WIDTH-1:0]     mem_data;
);

    //mem description
    logic [B_WIDTH-1:0] d_in;
    logic [B_WIDTH-1:0] q_fetch;

    logic [2**MEM_SIZE-1:0][B_WIDTH-1:0] mem_array;


    always_comb begin : readwrite_data_fetch
        //read
        mem_data <= (mem_read_en & ~mem_write_en) ? mem_fetch : 32'hz;
        // if (mem_read_en & ~mem_write_en == 1'b1) begin
        //     mem_data <= mem_fetch;
        // end

        //write
        d_in <= (~mem_read_en & mem_write_en) ? mem_data : 32'hz;
    end

    always_ff @( posedge clk ) begin : mem_read_write
        //read
        if (mem_read_en & ~mem_write_en == 1'b1) begin
            q_fetch <= mem_array[mem_addr];
        end

        //write
        if (~mem_read_en & mem_write_en == 1'b1) begin
            // mem_array[mem_addr] <= d_in;
            for (int i = (B_WIDTH/8)-1; i>=0; i--) begin
                if (write_byte_en[i]) mem_array[mem_addr][i*8+:8] <= d_in;
            end
        end
    end


endmodule
